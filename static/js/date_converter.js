window.convertDateFormat = function(inputDate) {
    const formattedDate = format(new Date(inputDate), 'yyyy-MM-dd'); 
    return moment(formattedDate, 'YYYY-MM-DD').format('YYYY-MM-DD');
};

document.addEventListener("DOMContentLoaded", function() {
    var languageBtn = document.getElementById("language-btn");
    var languageMenu = document.getElementById("language-menu");

    if (languageBtn) {
        languageBtn.addEventListener("click", function() {
            var computedStyle = window.getComputedStyle(languageMenu);
            if (computedStyle.display === "none" || computedStyle.display === "") {
                languageMenu.style.display = "block";
            } else {
                languageMenu.style.display = "none";
            }
        });
    }

    document.querySelectorAll('.dropdown-menu').forEach(function(menu) {
        menu.style.borderTop = 'none';
    });

    $(".like-btn").click(function() {
        var likeBtn = $(this);
        var comment_pk = likeBtn.data("comment-pk");
        var url = likeBtn.data("url");
        var csrf_token = "YOUR_CSRF_TOKEN_HERE"; 
        $.ajax({
            url: url,
            type: 'POST',
            data: { 'pk': comment_pk },
            headers: { "X-CSRFToken": csrf_token },
            dataType: 'json',
            success: function(data) {
                if (data.liked) {
                    likeBtn.addClass("liked");
                    likeBtn.text("Unlike");
                } else {
                    likeBtn.removeClass("liked");
                    likeBtn.text("Like");
                }
                var likesCountElement = likeBtn.siblings(".likes-count");
                likesCountElement.text(data.count);
            },
            error: function(xhr, errmsg, err) {
                console.log("Failed to send POST request.");
            }
        });
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
