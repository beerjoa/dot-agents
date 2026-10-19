const THEMES = {
    light: 'ccehnmniielbahkigdnafcjlbodlnbin',
    dark: 'kaajneiiilkiffigikfonphgemodkjah',
};
let queue = Promise.resolve();
let port;
let desiredMode;

async function applyMode(mode) {
    if (!Object.hasOwn(THEMES, mode)) throw new Error('Invalid theme mode');
    const other = await chrome.management.get(THEMES[mode === 'light' ? 'dark' : 'light']).catch(() => null);
    if (other && other.type !== 'theme') throw new Error('Expected an Omarchy theme');
    // Disable explicitly before enabling the next theme. DISABLE_BY_ANOTHER_EXTENSION
    // keeps Chrome's unused-theme collector from deleting the other palette.
    if (other?.enabled) await chrome.management.setEnabled(other.id, false);
    const target = await chrome.management.get(THEMES[mode]);
    if (target.type !== 'theme') throw new Error('Expected an Omarchy theme');
    if (!target.enabled) await chrome.management.setEnabled(target.id, true);
    await chrome.storage.local.set({status: {mode, themeId: target.id, error: null}});
}

function connect() {
    if (port) return;
    port = chrome.runtime.connectNative('dev.beerjoa.omarchy_browser_theme');
    port.postMessage({type: 'subscribe'});
    port.onMessage.addListener((message) => {
        queue = queue.then(() => {
            if (message.type !== 'palette') throw new Error('Invalid palette message');
            desiredMode = message.palette?.mode;
            return applyMode(desiredMode);
        }).catch((error) => chrome.storage.local.set({status: {error: String(error)}}));
    });
    port.onDisconnect.addListener(() => {
        const error = chrome.runtime.lastError?.message || 'Native host disconnected';
        port = null;
        void chrome.storage.local.set({status: {error}});
        void chrome.alarms.create('reconnect', {delayInMinutes: 0.5});
    });
}

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'reconnect') connect();
});
chrome.management.onInstalled.addListener((info) => {
    if (Object.values(THEMES).includes(info.id) && desiredMode) {
        queue = queue.then(() => applyMode(desiredMode))
            .catch((error) => chrome.storage.local.set({status: {error: String(error)}}));
    }
});
connect();
