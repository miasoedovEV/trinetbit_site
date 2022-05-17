const replace = (string) => {
    let arr = string.split('')
    for (let i = 0; i < arr.length; i++) {
        if (i === arr.length - 1) {
            break
        } else if (i !== 0) {
            arr[i] = '*'
        }
    }
    return arr.join('')
}

const wallet = document.getElementById('wallet')
const password = document.getElementById('password')
const changeWallet = document.getElementById('changeWallet')

wallet.value = replace(wallet.value)
password.value = replace(password.value)
changeWallet.value = replace(wallet.value)
