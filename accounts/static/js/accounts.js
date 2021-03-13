const usernameField = document.querySelector('#id_username');
const feedbackField = document.querySelector('.invalid-feedback');
usernameField.addEventListener("keyup", (e) => {

    console.log('777777', 77777);
    const usernameVal = e.target.value;

    usernameField.classList.remove("is-invalid");
    feedbackField.style.display = 'none';
    feedbackField.innerHTML ='<p> ${data.username_error}</>'

    if(usernameVal.length > 0){
        fetch('/validate-username',{
            body: JSON.stringify({username: usernameVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);
            if (data.username_error){
                usernameField.classList.add("is-invalid");
                feedbackField.style.display = 'block';
                feedbackField.innerHTML ='<p> ${data.username_error}</>'
            }
        });
      }
    });
    




