// Create the "Import" button element
var importButton = $('<button>', {
    'class': 'import-button',
    html: '<i class="fa fa-shopping-cart"></i> Import'
});

var popupContainer = $('<div>', {
    'class': 'popup-container',
    html: `
        <div class="popup">
            <div class="popup-content">
                <div class="popup-head">
                    <h3 class="popup-title">Trendyol Importer</h3>
                    <button class="close-button">&times;</button>
                </div> 
                <div class="popup-body">
                    <div class="lasttime">
                        <h4>Last Updated: <span>September 14, 2023, 3:30 PM</span></h4>
                    </div>
                    <div class="dropdown-items">
                        <div class="dropdown">
                            <div class="selected-option">
                                <span class="icon language-icon" style="background-image: url('images/flag.png');"></span>
                                <span class="option-text">Languages</span>
                            </div>
                            <div class="options">
                                <div class="option" data-value="turkish">
                                    <span class="icon flag-icon-turkish"></span>
                                    <span class="option-text">Turkish</span>
                                </div>
                                <div class="option" data-value="french">
                                    <span class="icon flag-icon-french"></span>
                                    <span class="option-text">French</span>
                                </div>
                                <div class="option" data-value="english">
                                    <span class="icon flag-icon-english"></span>
                                    <span class="option-text">English</span>
                                </div>
                                <div class="option" data-value="german">
                                    <span class="icon flag-icon-german"></span>
                                    <span class="option-text">German</span>
                                </div>
                            </div>
                        </div>
                    
                        <div class="dropdown">
                            <div class="selected-option">
                                <span class="icon currency-icon"></span>
                                <span class="option-text">Currency Selector</span>
                            </div>
                            <div class="options">
                                <div class="option" data-value="pounds">
                                    <span class="icon currency-icon-pounds"></span>
                                    <span class="option-text">Pounds</span>
                                </div>
                                <div class="option" data-value="euros">
                                    <span class="icon currency-icon-euros"></span>
                                    <span class="option-text">Euros</span>
                                </div>
                                <div class="option" data-value="turkish-lira">
                                    <span class="icon currency-icon-turkish-lira"></span>
                                    <span class="option-text">Turkish Lira</span>
                                </div>
                                <div class="option" data-value="usd">
                                    <span class="icon currency-icon-usd"></span>
                                    <span class="option-text">USD</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="list-head">
                        <h4>Import List</h4>
                        <h4 class="total-count">Products in Import List : <span>7/100</span></h4>
                    </div>

                    <div class="import-table">
                        <table style="width: 100%;">
                            <tbody>
                                <tr>
                                    <td>1</td>
                                    <td>Product A</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Product B</td>
                                    <td><button><i class="fa-solid fa-trash-can"></i></button></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="foot-button">
                        <button class="reset">Reset List</button>
                        <button class="export-csv">Export to CSV</button>
                    </div>
                        
                </div>

            </div> 
        </div>
    `
});

// Find the "product-price-container" element and prepend the button to it
var prcDscSpan = $('.product-price-container .prc-dsc');
var prcMainPopup = $('main#product-detail-app');
var langAttribute = $('html').attr('lang');


if (langAttribute === 'tr-TR') {
    // console.log('🚀 Language is Turkish. 🇹🇷');
    if (prcDscSpan.length > 0 || prcMainPopup.length > 0) {
        prcDscSpan.after(importButton);
        popupContainer.prependTo(prcMainPopup);
    }

    // When the "Import" button is clicked
    $('.import-button').click(function () {
        // Show the popup
        $('.popup-container').fadeIn();
    });

    // When the close button is clicked
    $('.close-button').click(function () {
        // Hide the popup
        $('.popup-container').fadeOut();
    });

    // Dropdown 
    $(".selected-option").click(function () {
        $(this).next(".options").toggle();
    });

    // Close dropdowns when clicking outside
    $(document).click(function (event) {
        if (!$(event.target).closest(".dropdown").length) {
            $(".options").hide();
        }
    });


}


