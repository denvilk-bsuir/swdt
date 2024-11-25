window.addEventListener("load", ()=>{
    let logoutBtn = document.getElementById("logout-button");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e)=>{
            document.getElementById("logout-form").submit();
        })
    }
})