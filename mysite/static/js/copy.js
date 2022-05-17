function copy_sum_paid() {
    text = document.getElementById('id-sum-paid').textContent
    navigator.clipboard.writeText(text.slice(0, -4));    
}

function copy_id_wallet() {
    navigator.clipboard.writeText("TQgYkeAgXkc4LHC9GqF4xHpCr8d8xZmK6K");    
}

const btSumm = document.getElementById('bt-sum-paid')
const btWallet = document.getElementById('bt-id-wallet')
btSumm.addEventListener("click", copy_sum_paid);
btWallet.addEventListener("click", copy_id_wallet);