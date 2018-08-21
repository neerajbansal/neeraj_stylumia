const baseUrl = 'http://' + window.location.host + '/';

function clearLocalStorage() {
    window.localStorage.clear();
    window.location.href = baseUrl;
}

function showLoader() {
    $(document).ready(function () {
        $('#loader').show();
    })
}

function hideLoader() {
    $(document).ready(function () {
        $('#loader').hide();
    })
}

function isLoggedIn() {
    if (!window.localStorage.getItem('access_token')) {
        clearLocalStorage();
        return false;
    }
    else {
        return true;
    }
}

function ajaxWrapper(method, url, dataToSend, callback) {
    const token = window.localStorage.getItem('access_token');
    $.ajax({
        type: method,
        url: baseUrl + url,
        data: dataToSend ? JSON.stringify(dataToSend) : null,
        contentType: 'application/json',
        headers: {
            "Authorization": "JWT " + token
        },
        success: function (data) {
            return callback(null, data);
        },
        error: function (error) {
            return callback(error);
        }
    });
}