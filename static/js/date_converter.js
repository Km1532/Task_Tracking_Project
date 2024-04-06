window.convertDateFormat = function(inputDate) {
    const formattedDate = format(new Date(inputDate), 'yyyy-MM-dd'); 
    return moment(formattedDate, 'YYYY-MM-DD').format('YYYY-MM-DD');
};

document.addEventListener("DOMContentLoaded", function() {
    var languageBtn = document.getElementById("language-btn");
    var languageMenu = document.getElementById("language-menu");

    languageBtn.addEventListener("click", function() {
        var computedStyle = window.getComputedStyle(languageMenu);
        if (computedStyle.display === "none" || computedStyle.display === "") {
            languageMenu.style.display = "block";
        } else {
            languageMenu.style.display = "none";
        }
    });

    // Функція для зміни мови
    window.changeLanguage = function(language) {
        var selectedLanguage = language;
        var ukFlagUrl = "/static/images/ukraine.png";
        var usFlagUrl = "/static/images/usa_flag.png";
               
        // Приклад встановлення мови у cookie
        document.cookie = "selectedLanguage=" + selectedLanguage + "; expires=Thu, 31 Dec 2099 23:59:59 UTC; path=/";
        
        // Вивід вибраної мови у консоль
        console.log("Обрана мова:", selectedLanguage);
        
        // Здійснюємо зміну мови відповідно до вибраної мови
        var languageIcon = languageBtn.querySelector("img");
        if (language === 'uk') {
            languageIcon.src = ukFlagUrl;
        } else if (language === 'en') {
            languageIcon.src = usFlagUrl;
        }

        // Закриття вікна мови
        languageMenu.style.display = "none";
    }
});

window.changeLanguage = function(language) {
    var selectedLanguage = language;

    // AJAX-запит для збереження мови у сесії
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_language/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Перезавантажуємо сторінку після зміни мови
            window.location.reload();
        }
    };
    xhr.send(JSON.stringify({ language: selectedLanguage }));
}
