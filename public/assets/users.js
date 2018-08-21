if (isLoggedIn()) {
    var roles = {};
    var users = {};

    var getRoles = new Promise((resolve, reject) => {
        ajaxWrapper('GET', 'api/role', null, function (err, data) {
            if (err) {
                alert('Your session is expired, please login to continue...');
                reject();
            }
            else {
                roles = data.roles;
                resolve('roles fetching done');
            }
        })
    })

    var getUsers = new Promise((resolve, reject) => {
        ajaxWrapper('GET', 'api/user', null, function (err, data) {
            if (err) {
                alert('Your session is expired, please login to continue...');
                reject();
            }
            else {
                users = data.users;
                resolve('users fetching done');
            }
        })
    })

    var deleteUser = function (id) {
        var url = 'api/user/' + id;
        showLoader();
        ajaxWrapper('DELETE', url, null, function (err, data) {
            hideLoader();
            if (err) {
                alert(err.responseJSON.message);
            }
            else {
                alert(data.message);
                users = users.filter((user) => { return user.id != id });
                renderUserTable(users, roles);
            }
        })
    }

    var updateUser = function (id) {
        var dataToSend = {};
        var name = $('#updateName').val();
        var role = $('#updateRole').val();
        var bio = $('#updateBio').val();
        var address = $('#updateAddress').val();
        var email = $('#updateEmail').val();
        dataToSend["id"] = id;
        dataToSend["name"] = name;
        dataToSend["role_id"] = Number(role);
        dataToSend["bio"] = bio;
        dataToSend["address"] = address;
        dataToSend["email"] = email;

        showLoader();
        ajaxWrapper('POST', 'api/user/update', dataToSend, function (err, data) {
            hideLoader();
            if (err) {
                alert(err.responseJSON.message);
            }
            else {
                alert(data.message);
                var userLen = users.length;
                for (var i = 0; i < userLen; i++) {
                    if (users[i].id == id) {
                        users[i] = dataToSend;
                    }
                }
                renderUserTable(users, roles);
            }
        })

    }

    var editUser = function (id) {
        for (var user in users) {
            if (users[user]['id'] != id) {
                $('#card' + users[user]['id']).addClass('disabledDiv');
            }
        }
        $('#card' + id).empty();
        var userToEdit = users.filter((user) => { return user.id == id })[0];
        var cards = '';
        cards += '<div class="card-body">';
        cards += '<input id="updateName" placeholder="Name" type="text" class="form-control" value="' + userToEdit['name'] + '"></input>';
        cards += '<select id="updateRole" class="form-control">';
        for (var role in roles) {
            cards += ' <option value="' + roles[role]['id'] + '">' + roles[role]['role'] + '</option>';
        }
        cards += '</select>';
        cards += '<input id="updateBio" placeholder="Brief Bio" type="text" class="form-control" value="' + userToEdit['bio'] + '"></input>';
        cards += '<input id="updateAddress" placeholder="Address" type="text" class="form-control" value="' + userToEdit['address'] + '"></input>';
        cards += '<input id="updateEmail" placeholder="Email" type="text" class="form-control" value="' + userToEdit['email'] + '"></input>';
        cards += '<button type="button" onclick="updateUser(' + id + ')" class="btn btn-link">Save</button>';
        cards += '<button type="button" onclick="onEditCancel(' + id + ')" class="btn btn-link">Cancel</button>';
        cards += '</div>';
        $('#card' + id).append(cards);
    }

    function onEditCancel(id) {
        for (var user in users) {
            if (users[user]['id'] != id) {
                $('#card' + users[user]['id']).removeClass('disabledDiv');
            }
        }
        renderUserTable(users, roles);
    }
    $(document).ready(function () {
        var name = window.localStorage.getItem('name');
        $('#nameSpan span').html("Hi " + name);
    });

    getRoles.then((data) => {
        getUsers.then(() => {
            hideLoader();
            renderUserTable(users, roles);
        }).catch((err) => {
            hideLoader();
            clearLocalStorage();
        });
    }).catch((err) => {
        hideLoader();
        clearLocalStorage();
    });


    function renderUserTable(usersObj, roleObj) {
        $('#userListTable').empty();

        var cards = '';
        var user_id = window.localStorage.getItem('user_id');
        var role_id = window.localStorage.getItem('role_id');
        for (var user in usersObj) {
            var role = roleObj.filter((role) => { return role.id == usersObj[user]['role_id'] })[0];
            cards += '<div class="col-md-4">'
            cards += '<div id="card' + usersObj[user]['id'] + '" class="card" style="width: 18rem;margin-top:20px;">';
            cards += '<div class="card-body">';
            cards += '<h5 class="card-title">' + usersObj[user]['name'] + '</h5>';
            cards += '<h6 class="card-subtitle mb-2 text-muted">' + role['role'] + '</h6>';
            cards += '<p class="card-text">' + usersObj[user]['bio'] + '</p>';
            cards += '<b>Area: </b>' + usersObj[user]['address'] + '</br>';
            cards += '<b>E-mail: </b>' + usersObj[user]['email'] + '</br>';
            if (role_id > usersObj[user]['role_id']) {
                cards += '<button type="button" style= "color:red;" onclick="deleteUser(' + usersObj[user]['id'] + ')" class="btn btn-link">Delete</button>';
            }
            if (role_id > usersObj[user]['role_id'] || user_id == usersObj[user]['id']) {
                var id = usersObj[user]['id'];
                cards += '<button type="button" onclick="editUser(' + id + ')" class="btn btn-link">Edit</button>';
            }
            cards += '</div>';
            cards += '</div>';
            cards += '</div>';
        }
        $('#userListTable').append(cards);
    }
}

