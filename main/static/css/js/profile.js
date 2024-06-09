document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('editButton');
    const cancelButton = document.getElementById('cancelButton');
    const profileInfo = document.querySelector('.profile-info');
    const profileEdit = document.querySelector('.profile-edit');
    const profileForm = document.getElementById('profileForm');

    editButton.addEventListener('click', function () {
        profileInfo.style.display = 'none';
        profileEdit.style.display = 'block';
    });

    cancelButton.addEventListener('click', function () {
        profileEdit.style.display = 'none';
        profileInfo.style.display = 'block';
    });

    profileForm.addEventListener('submit', function (event) {
        event.preventDefault();

        
        const formData = new FormData(profileForm);
        const fullName = formData.get('fullName');
        const fullAddress = formData.get('fullAddress');
        const fullnumber = formData.get('fullnumber');
        const email = formData.get('email');

        
        setTimeout(() => {
        
            const success = true;

            if (success) {
                document.getElementById('fullName').innerText = fullName;
                document.getElementById('fullAddress').innerText = fullAddress;
                document.getElementById('fullnumber').innerText = fullnumber;
                document.getElementById('email').innerText = email;
            }

            profileEdit.style.display = 'none';
            profileInfo.style.display = 'block';
        }, 1000);
    });
});
