$(document).on('DOMContentLoaded', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var currentTab = tabs[0];
        chrome.tabs.update(currentTab.id, { url: "https://www.trendyol.com" });
    });

    var importButton = $('<button class="import-button"><i class="fa fa-shopping-cart"></i> Import</button>');

    // Prepend the button to the "prc-dsc" element
    $('.product-price-container .prc-dsc').before(importButton);
    

});
