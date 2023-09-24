chrome.runtime.onInstalled.addListener(function (details) {
    if (details.reason === 'install' || details.reason === 'update') {
        console.log("The extension has been installed or updated.");
    }
});
