
$(document).ready(function() {
    $("#add").click(function() {
        $("#my-form").show(); 
    });
    $("#add").dblclick(function() {
        $("#my-form").hide(); 
    });


    $("#my-form").submit(function() {
        $("#my-form").hide();  
    });
});


//toggling inputs
function toggleInput() {
    var selectElement = document.getElementById("routingType");
    var inputContainer = document.getElementById("inputContainer");
    
    if (selectElement.value === "pre-routing") {
        inputContainer.innerHTML = `
        <input type="text" name="routing" placeholder="prerouting"><br>
        <input type="text" name="source_ip" placeholder="Source IP"><br>
        <input type="text" name="source_port" placeholder="Source Port"><br>
        <input type="text" name="protocol" placeholder="Protocol"><br>
        <input type="text" name="destination_ip" placeholder="Destination IP"><br>
        <input type="text" name="destination_port" placeholder="Destination Port"><br>
    `;
    } else if (selectElement.value === "post-routing") {
        inputContainer.innerHTML = `
        <input type="text" name="routing" placeholder="postrouting"><br>
        <input type="text" name="source_ip" placeholder="Source IP"><br>
        <input type="text" name="destination_ip" placeholder="Destination IP"><br>
    `;
    } else if (selectElement.value === "both") {
        inputContainer.innerHTML = `
        <input type="text" name="routing" placeholder="both"><br>
        <input type="text" name="source_ip" placeholder="Source IP"><br>
        <input type="text" name="source_port" placeholder="Source Port"><br>
        <input type="text" name="protocol" placeholder="Protocol"><br>
        <input type="text" name="destination_ip" placeholder="Destination IP"><br>
        <input type="text" name="destination_port" placeholder="Destination Port"><br>
    `;
    
    } else {
        inputContainer.innerHTML = ''; // Clear the input field if neither option is selected
    }
}


//popup

const popup = document.getElementById('custom-popup');
const policyId = document.getElementById('policy-id');
const confirmButton = document.getElementById('popup-confirm');
const cancelButton = document.getElementById('popup-cancel');

function showPopup(id) {
    policyId.textContent = id;
    popup.style.display = 'block';
}
function hidePopup() {
    popup.style.display = 'none';
}
cancelButton.addEventListener('click', function () {
    hidePopup();
});

//get cookie
function getCookie(name) {
    var value = "; " + document.cookie;

    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
//for deleting routes
function deleteRow2(button,types) {
            const object_id = $(button).data('object-id');
            showPopup(object_id);
            confirmButton.addEventListener('click', function () { 
                $.ajax({
                    url: `/delete/${types}/${object_id}/`, 
                    type: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'), 
                    },
                    success: function(response) {
                        $(button).closest('tr').remove();
                    },
                    error: function(xhr, status, error) {
                        console.error(error);
                    }

                });
            //}
       
            hidePopup();
        });

        }






//edit

$(document).ready(function() {
    function enableEditing(cells) {
        cells.each(function() {
            $(this).prop('contenteditable', true);
        });
    }

    $(".edit").click(function() {
        const sav = $(this).closest('tr').find('.save');
        sav.show();
        const cells = $(this).closest('tr').find('td[contenteditable="false"]');
        enableEditing(cells);
    });
});


//save
function myFunction(val) { 
    routing=val; 
  } 


$(document).ready(function() {


    function enablesaving(saved_id,values_changed,sav_close,cells) {
        
        function disableEditing(cells) {
            cells.each(function() {
                $(this).prop('contenteditable', false);
            });
        }


        console.log(saved_id)
        var myList = []; 
        values_changed.each(function() {
           var a=$(this).text().replace(/\n/g, '').trim().replace(/\s+/g, ' ');
           myList.push(a);
           

        });
        mydata=myList.pop()
        console.log(myList);
        console.log(routing);
        $.ajax({
            type: 'POST',
            url: `/save/${routing}/${saved_id}/`,
            data: JSON.stringify(myList),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), 
            },
            success: function (response) {
                
                console.log(response);
                sav_close.hide();
                disableEditing(cells);
                
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        });

    }
    $(".save").click(function() {
        const saved_id = $(this).data('object-id');
        const values_changed = $(this).closest('tr').find('td');
        const sav_close = $(this).closest('tr').find('.save');
        const cells = $(this).closest('tr').find('td[contenteditable="true"]');
        enablesaving(saved_id,values_changed,sav_close,cells)
        



    });
});



//user views


//popup
var userGroup = document.getElementById('user-group-data')
var admingroup = userGroup.getAttribute('data-user-group');

function showadmin() {
    userGroup.style.display = 'block';
}
function hideadmin() {
    userGroup.style.display = 'none';
}

if (admingroup == "READ_WRITE" )  {
    showadmin()
}


//errormsg
document.addEventListener("DOMContentLoaded", function() {
    const errorPopup = document.getElementById("error-popup");
    const errorMessage = document.getElementById("error-msg");

    const err_msg = errorPopup.getAttribute("data-error-msg")
    errorMessage.textContent=err_msg;
    if (err_msg !==0 && err_msg.trim() !== "None") {
        console.log("hello")
        errorPopup.style.display = 'block';
    }

    document.getElementById("close-popup").addEventListener("click", function () {
        errorPopup.style.display = 'none';
    });
});

// Get the modal and buttons
var loginModal = document.getElementById("loginModal");
var server_details_btn = document.getElementById("server_details_btn");
var close_btn = document.getElementById("close_btn");



// Open the login modal when the button is clicked
server_details_btn.onclick = function() {

    loginModal.style.display = "block";
}

// Close the login modal when the close button is clicked
close_btn.onclick = function() {
    loginModal.style.display = "none";
}

// Close the login modal if the user clicks outside of it
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
}

// Handle login form submission
var loginForm = document.getElementById("loginForm");
loginForm.onsubmit = function(e) {
    e.preventDefault();
    // Add your login form submission logic here
    // You can use AJAX to submit the form data to your Django view
}