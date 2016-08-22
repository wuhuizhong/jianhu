$('.tab').on('click', function(event) {
    // event.preventDefault();
    var id = this.id;
    // alert(id)
    switch(id){
        case '1':
            // location.href = "../index.html";
            break;
        case '2':             
            location.href = "/chat/msg";
            break;
        case '3':                
            location.href = "/user/me";
            break;
    }
});
