<script>
    function togglePasswordVisibility() {
        var passwordInput = document.getElementById('password');
        var toggleIcon = document.getElementById('togglePasswordIcon');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.className = 'ri-eye-off-line';
        } else {
            passwordInput.type = 'password';
            toggleIcon.className = 'ri-eye-line';
        }
    }
</script>
