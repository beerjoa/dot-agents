local links = require("../windows_file_links")
local root = "C:\\Work\\repo"

local cases = {
	{ "C:/Work/repo/src/main.rs", root, { path = "src/main.rs" } },
	{ "C:\\Work\\repo\\src\\main.rs:12:3", root, { path = "src/main.rs", line = 12, column = 3 } },
	{ "c:/work/REPO/src/Main.rs", root, { path = "src/Main.rs" } },
	{ "C:/Work/repo/src/main.rs#L12C5", root, { path = "src/main.rs", line = 12, column = 5 } },
	{ "C:/Work/repo/src/main.rs#L12-L20", root, { path = "src/main.rs", line = 12, end_line = 20 } },
	{ "C:/Work/repo/src/main.rs:12-20", root, { path = "src/main.rs", line = 12, end_line = 20 } },
	{ "file:///C:/Work/repo/src/main.rs#L12", root, { path = "src/main.rs", line = 12 } },
	{ "file:///C%3A/Work/repo/src/main.rs", root, { path = "src/main.rs" } },
	{ "C:/Work/repo/read%20me.md", root, { path = "read me.md" } },
	{ "C:/Work/repo/한글.md", root, { path = "한글.md" } },
	{ "C:/Work/repo/%ED%95%9C%EA%B8%80.md", root, { path = "한글.md" } },
	{ "C:/Work/repo/notes%23one.md", root, { path = "notes#one.md" } },
	{ "C:/Work/repo/discount%25off.md", root, { path = "discount%off.md" } },
	{ "C:/Work/repo/LICENSE", root, { path = "LICENSE" } },
	{ "C:/Work/repo/main.rs", "C:/Work/repo/", { path = "main.rs" } },
	{ "C:/src/main.rs", "C:\\", { path = "src/main.rs" } },
	{ "C:/Work/repo/main.rs", "C:/Work/repo", { path = "main.rs" } },
	{ "  C:/Work/repo/main.rs:1  ", root, { path = "main.rs", line = 1 } },

	{ "C:/Work/repo2/main.rs", root, false },
	{ "C:/Work/other/main.rs", root, false },
	{ "D:/Work/repo/main.rs", root, false },
	{ "C:/Work/repo/main.rs", nil, false },
	{ "C:/Work/repo/main.rs", "/work/repo", false },
	{ "C:/Work/repo/../secret.md", root, false },
	{ "C:\\Work\\repo\\..\\secret.md", root, false },
	{ "C:/Work/repo/%2e%2e/secret.md", root, false },
	{ "C:/Work/repo/%2e%2e%5csecret.md", root, false },
	{ "C:/Work/repo/src/./main.rs", root, false },
	{ "C:/Work/repo/src//main.rs", root, false },
	{ "C:/Work/repo/folder/", root, false },
	{ "C:/Work/repo", root, false },
	{ "C:", root, false },
	{ "C:/", root, false },
	{ "C:main.rs", root, false },
	{ "C:/Work/repo/main.rs:0", root, false },
	{ "C:/Work/repo/main.rs:12:0", root, false },
	{ "C:/Work/repo/main.rs#L0", root, false },
	{ "C:/Work/repo/main.rs#L20-L12", root, false },
	{ "C:/Work/repo/main.rs:20-12", root, false },
	{ "C:/Work/repo/main.rs:stream", root, false },
	{ "C:/Work/repo/main.rs%3Astream", root, false },
	{ "C:/Work/repo/bad%ZZ.md", root, false },
	{ "C:/Work/repo/bad%FF.md", root, false },
	{ "C:/Work/repo/bad%00.md", root, false },
	{ "file://server/share/main.rs", root, false },
	{ "file:///C:/Work/repo/main.rs?query=1", root, false },
	{ "\\\\server\\share\\main.rs", root, false },
	{ "C:\\?\\Work\\repo\\main.rs", root, false },

	{ "src/main.rs:12:3", root, { path = "src/main.rs", line = 12, column = 3 } },
	{ "src/main.rs#L12-L20", root, { path = "src/main.rs", line = 12, end_line = 20 } },
	{ "/work/repo/src/main.rs", "/work/repo", { path = "src/main.rs" } },
	{ "file:///work/repo/README", "/work/repo", { path = "README" } },
	{ "/elsewhere/main.rs", "/work/repo", { path = "/elsewhere/main.rs", outside = true } },
	{ "zeron-file:notes/read%20me.md", root, { path = "notes/read me.md" } },
	{ "../secret.md", root, false },
	{ "zeron-file:../secret.md", root, false },
	{ "https://example.com/main.rs", root, false },
	{ "mailto:user@example.com", root, false },
	{ "", root, false },
}

local failures = {}
for i, case in cases do
	local actual = links.resolve(case[1], case[2])
	local expected = case[3]
	local ok = if expected == false then actual == nil else actual ~= nil
	if ok and expected ~= false then
		for key, value in expected do
			ok = ok and actual[key] == value
		end
		for key, value in actual do
			ok = ok and expected[key] == value
		end
	end
	if not ok then
		table.insert(failures, `case {i}: {case[1]}`)
	end
end

local link = links.link("notes/read me.md")
assert(links.path_of(string.match(link, "%((.*)%)$") :: string) == "notes/read me.md", "Mention round-trip")
assert(links.chip("src/main.rs", root), "Relative file chip")
assert(not links.chip("/elsewhere/main.rs", "/work/repo"), "Outside files stay outside")
if #failures > 0 then
	error(`{#failures}/{#cases} path cases failed:\n{table.concat(failures, "\n")}`)
end
assert(links.chip("C:/Work/repo/main.rs", root), "Windows file chip uses the corrected resolver")
print(`PASS: {#cases} path cases; mention round-trip and file-chip integration`)
