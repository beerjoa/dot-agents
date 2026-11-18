-- Based on Zeron beta 0.3.7's screens/chat/file_links.luau (MIT).
-- Upstream: zeronsh/zeron, f6a9bbfc29796cb90389ddd8e2e3bdcd8996829b.
-- See ZERON-LICENSE and README.md for provenance.
local M = {}

function M.link(path: string, dir: boolean?): string
	local bare = string.gsub(path, "/+$", "")
	local name = string.match(bare, "([^/]+)$") or bare
	local label = string.gsub(name, "[\\%[%]`]", function(c: string): string
		return "\\" .. c
	end)
	local target = string.gsub(bare .. (if dir then "/" else ""), "[^%w%-%._~/]", function(c: string): string
		return string.format("%%%02X", string.byte(c))
	end)
	return `[{label}](zeron-file:{target})`
end

function M.path_of(link: string): string?
	local target = string.match(link, "^zeron%-file:(.+)$")
	if not target then
		return nil
	end
	local ok = true
	local path = string.gsub(target, "%%(%x%x)", function(h: string): string
		return string.char(tonumber(h, 16) :: number)
	end)
	local bare = string.gsub(path, "/$", "")
	if bare == "" or string.find(bare, "//", 1, true) then
		ok = false
	end
	for part in string.gmatch(bare, "[^/]+") do
		if part == "." or part == ".." then
			ok = false
		end
	end
	if not ok or string.sub(path, 1, 1) == "/" or string.find(path, "\\", 1, true) then
		return nil
	end
	return path
end

export type Resolved = { path: string, line: number?, column: number?, end_line: number?, outside: boolean? }

local function decode(raw: string): string?
	local bad = false
	local out = string.gsub(raw, "%%(..)", function(h: string): string
		local n = if string.match(h, "^%x%x$") then tonumber(h, 16) else nil
		if not n then
			bad = true
			return ""
		end
		return string.char(n)
	end)
	if bad or not utf8.len(out) then
		return nil
	end
	return out
end

local function encode(path: string): string
	return (string.gsub(path, "[^%w%-%._~/]", function(c: string): string
		return string.format("%%%02X", string.byte(c))
	end))
end

local function clean(path: string): boolean
	if string.find(path, "[\\%?%c]") then
		return false
	end
	local index = 0
	for part in string.gmatch(path .. "/", "([^/]*)/") do
		index += 1
		if (part == "" and index ~= 1) or part == "." or part == ".." then
			return false
		end
	end
	return true
end

local function file_name(path: string): string
	return string.match(path, "([^/]*)$") or path
end

local function positive(v: string): number?
	local n = if string.match(v, "^%d+$") then tonumber(v) else nil
	return if n and n > 0 then n else nil
end

local function line_column(v: string): (number?, number?)
	local line, column = string.match(v, "^(%d+)C(%d+)$")
	if line then
		return tonumber(line), tonumber(column)
	end
	if string.match(v, "^%d+$") then
		return tonumber(v), nil
	end
	return nil, nil
end

local function fragment(target: string): (string | false, number?, number?, number?)
	local path_, frag_ = string.match(target, "^(.*)#([^#]*)$")
	if not path_ or not frag_ then
		return target, nil, nil, nil
	end
	local path, frag = path_ :: string, frag_ :: string
	if frag == "" then
		return path, nil, nil, nil
	end
	if string.find(frag, "/", 1, true) then
		return target, nil, nil, nil
	end
	local rest = string.match(frag, "^L(.*)$") :: string?
	if not rest then
		return path, nil, nil, nil
	end
	local start = string.match(rest, "^([^%-]*)%-") :: string?
	local finish = string.match(rest, "^[^%-]*%-(.*)$") :: string?
	local line, column = line_column(start or rest)
	if not line then
		return path, nil, nil, nil
	end
	if line == 0 or column == 0 then
		return false, nil, nil, nil
	end
	if finish then
		local e, ec = line_column((string.match(finish, "^L(.*)$") :: string?) or finish)
		if not e then
			return path, nil, nil, nil
		end
		if e < line or ec == 0 then
			return false, nil, nil, nil
		end
		return path, line, column, if e > line then e else nil
	end
	return path, line, column, nil
end

local function suffix(target: string): (string | false, number?, number?, number?)
	local before_ = string.match(target, "^(.*):[^:]*$") :: string?
	if not before_ then
		return target, nil, nil, nil
	end
	local before = before_ :: string
	local last = string.sub(target, #before + 2)
	local a = string.match(last, "^([^%-]*)%-") :: string?
	local b = string.match(last, "^[^%-]*%-(.*)$") :: string?
	if a and b then
		if not string.match(a, "^%d+$") or not string.match(b, "^%d+$") then
			return target, nil, nil, nil
		end
		local start, finish = tonumber(a) :: number, tonumber(b) :: number
		if start == 0 or finish < start then
			return false, nil, nil, nil
		end
		return before, start, nil, if finish > start then finish else nil
	end
	if string.match(last, "^%d+$") and tonumber(last) == 0 then
		return false, nil, nil, nil
	end
	local n = positive(last)
	if not n then
		return target, nil, nil, nil
	end
	local before2 = string.match(before, "^(.*):[^:]*$") :: string?
	if before2 then
		local mid = string.sub(before, #before2 + 2)
		local line = positive(mid)
		if line then
			return before2, line, n, nil
		end
		if string.match(mid, "^%d+$") and tonumber(mid) == 0 then
			return false, nil, nil, nil
		end
	end
	return before, n, nil, nil
end

local function inside(path: string, root: string?): string?
	if not root or root == "" then
		return nil
	end
	local windows = string.match(path, "^%a:/") ~= nil
	local r = if windows then string.gsub(root, "\\", "/") else root
	r = string.gsub(r, "/+$", "")
	local compared = if windows then string.lower(path) else path
	local owner = if windows then string.lower(r) else r
	if string.sub(compared, 1, #owner + 1) ~= owner .. "/" then
		return nil
	end
	local rest = string.sub(path, #r + 2)
	return if rest ~= "" then rest else nil
end

function M.chip(target: string, root: string?): boolean
	local r = M.resolve(target, root)
	return r ~= nil and not r.outside
end

function M.resolve(target: string, root: string?): Resolved?
	target = string.match(target, "^%s*(.-)%s*$") or target
	if target == "" then
		return nil
	end
	local mention = string.match(target, "^zeron%-file:(.*)$")
	if mention then
		local path = decode(mention)
		if not path or encode(path) ~= mention or string.sub(path, -1) == "/" or string.find(path, ":", 1, true) or not clean(path) or string.sub(path, 1, 1) == "/" then
			return nil
		end
		return { path = path }
	end
	local file_url = string.sub(target, 1, 7) == "file://"
	local raw = target
	if file_url then
		local rest = string.sub(target, 8)
		if string.sub(rest, 1, 1) ~= "/" or string.find(rest, "?", 1, true) then
			return nil
		end
		raw = rest
	elseif string.find(target, "://", 1, true) or string.sub(target, 1, 7) == "mailto:" then
		return nil
	end
	local p1, line1, column1, end1 = fragment(raw)
	if not p1 then
		return nil
	end
	local p2, line2, column2, end2 = suffix(p1)
	if not p2 then
		return nil
	end
	local decoded = if string.find(p2, "%", 1, true) then decode(p2) else p2
	local path = decoded or p2
	if file_url and string.match(path, "^/%a:[/\\]") then
		path = string.sub(path, 2)
	end
	local windows = string.match(path, "^%a:[/\\]") ~= nil
	if windows then
		if not decoded or string.find(path, ":", 3, true) then
			return nil
		end
		path = string.gsub(path, "\\", "/")
	end
	if path == "" or not clean(path) then
		return nil
	end
	local line, column = line1 or line2, column1 or column2
	local end_line = if line1 then end1 else end2
	if windows then
		local rel = inside(path, root)
		if not rel then
			return nil
		end
		return { path = rel, line = line, column = column, end_line = end_line }
	end
	if string.sub(path, 1, 1) == "/" then
		if #path == 1 or string.sub(path, 1, 2) == "//" or string.sub(path, -1) == "/" or (not file_url and not string.find(file_name(path), ".", 1, true)) then
			return nil
		end
		local rel = inside(path, root)
		if rel then
			return { path = rel, line = line, column = column, end_line = end_line }
		end
		return { path = path, line = line, column = column, end_line = end_line, outside = true }
	end
	if file_url or string.sub(path, 1, 1) == "~" or string.match(path, "^%a[%w%+%-%.]*:") then
		return nil
	end
	if not string.find(file_name(path), ".", 1, true) then
		return nil
	end
	return { path = path, line = line, column = column, end_line = end_line }
end

return M
