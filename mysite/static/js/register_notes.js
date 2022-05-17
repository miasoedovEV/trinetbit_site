const width = window.outerWidth
const input = document.getElementById('api');
const keyInput = document.getElementById('key');
const userNameInput = document.getElementById("userName")
const emailInput = document.getElementById('email')
const walletInput = document.getElementById('wallet')
const passwordInput = document.getElementById('password')
const repeatPasswordInput = document.getElementById('repeatPassword')

const addListener = (input, group) => {
    input.addEventListener('focus', (event) => {
        const group1 = document.getElementsByClassName(group)
        for(i = 0; i < group1.length; i++) {
            group1[i].classList.add('show')
        }
    });
}

if (width > 1900) {
    addListener(input, 'group1-desc')

    addListener(keyInput, 'group1-desc')

    addListener(userNameInput, 'group2-desc')

    addListener(emailInput, 'group3-desc')

    addListener(walletInput, 'group4-desc')

    addListener(passwordInput, 'group5-desc')

    addListener(repeatPasswordInput, 'group6-desc')

} else {
    addListener(input, 'group1-mobile')

    addListener(keyInput, 'group1-mobile')

    addListener(userNameInput, 'group2-mobile')

    addListener(emailInput, 'group3-mobile')

    addListener(walletInput, 'group4-mobile')

    addListener(passwordInput, 'group5-mobile')

    addListener(repeatPasswordInput, 'group6-mobile')
}

