
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



function getCookie(name) {
    var value = "; " + document.cookie;

    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
//for deleting routes
function deleteRow2(button,types) {
            const object_id = $(button).data('object-id');
            const res = confirm("Do you want to policy id delete"  + object_id+ "?")  
            if (res == true){
                console.log(object_id)
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
            }
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



$(document).ready(function() {
    function enablesaving(values_changed) {
        const saved_id = $(".save").data('object-id');
        var myList = []; 
        values_changed.each(function() {
           var a=$(this).text().replace(/\n/g, '').trim().replace(/\s+/g, ' ');
           myList.push(a);
           

        });
        mydata=myList.pop()
        console.log(myList);
        $.ajax({
            type: 'POST',
            url: `/save/${saved_id}/`,
            data: JSON.stringify(myList),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), 
            },
            success: function (response) {
                console.log(response);
                
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        });
        





    }



    $(".save").click(function() {
        const values_changed = $(this).closest('tr').find('td');
        enablesaving(values_changed)
    });
});


