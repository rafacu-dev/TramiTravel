
var element_id;

$(document).ready(function () {
    $('.imagen-document').on('change', function (e) {
        element_id = e.target.id.substring('imagen-document-'.length);
        consumerAPI();
    });
});




function consumerAPI(){
    const url = 'https://api.accurascan.com/api/v4/ocr';
    
    if(document.getElementById(`imagen-document-${element_id}`).files.length == 0){return;}
    const file = document.getElementById(`imagen-document-${element_id}`).files[0];
    const formData = new FormData();
    formData.append('country_code', 'USA');
    formData.append('card_code', 'MRZ');
    formData.append('scan_image', file);

    const headers = {
        'Api-Key': '15610306389qH4ll3CJ8cBuo5zFlSEbDU1cIBHn9yEeLRgwd5R',
    };
    
    document.getElementById("processing_document_image").classList.remove("hidden");

    fetch(url, {
    method: 'POST',
    headers: headers,
    body: formData,
    })
    .then(response => response.json())
    .then(data => showResult(data))
    .catch(error => showError(error))
}


function showError(e) {
    console.error(e);
    document.getElementById("processing_document_image").classList.add("hidden");
    if(language === "es"){
        alert("Error al leer documento.");
    }else{
        alert("Error reading document.");
    }
}

function showResult(data) {
    const result = data.data.MRZdata;
    console.log(result);
    document.getElementById("processing_document_image").classList.add("hidden");

    if(data.Status !== "Success"){
        if(language === "es"){
            alert("Error al leer documento.");
        }else{
            alert("Error reading document.");
        }
    }
    else{
        if(result.document_type == "P" || result.document_type == "C1"){
            if(!element_id.includes("secondary-")){

                if(result.document_type == "P"){
                    $(`#type-document-primary-${element_id}`).val("Passport");
                }
                else {
                    $(`#type-document-primary-${element_id}`).val("U.S. Permanent Resident Card");
                }
                
                var firstName = result.first_name.split(" ")
                $(`#firstName-${element_id}`).val(firstName[0]);
                if(firstName.length > 1){
                    $(`#middleName-${element_id}`).val(firstName[1]);
                }
                else{
                    $(`#middleName-${element_id}`).val("");
                }

                var lastName = result.last_name.split(" ")
                $(`#lastName-${element_id}`).val(lastName[0]);
                if(lastName.length > 1){
                    $(`#motherLastName-${element_id}`).val(lastName[1]);
                }
                else{
                    $(`#motherLastName-${element_id}`).val("");
                }
                
                const birthDate = result.date_of_birth;
                let year_birthDate = parseInt(birthDate.substring(0, 2));

                if (year_birthDate >= 0 && year_birthDate <= 23) {
                    year_birthDate += 2000; // Siglo XXI
                } else {
                    year_birthDate += 1900; // Siglo XX
                }
                var month_birthDate = birthDate.substring(2, 4);
                var day_birthDate = birthDate.substring(4, 6);
                $(`#dateBirth-${element_id}`).val(`${month_birthDate}/${day_birthDate}/${year_birthDate}`);

                if(result.sex == "F"){
                    $(`input[name=gender-${element_id}]:eq(1)`).prop('checked', true);
                }else {
                    $(`input[name=gender-${element_id}]:eq(0)`).prop('checked', true);
                }

                $(`#number-document-primary-${element_id}`).val(result.document_no);

                const expirationDate = result.date_of_expiry;
                let year_expirationDate = "20" + expirationDate.substring(0, 2);
                var month_expirationDate = expirationDate.substring(2, 4);
                var day_expirationDate = expirationDate.substring(4, 6);
                $(`#expiration-document-primary-${element_id}`).val(`${month_expirationDate}/${day_expirationDate}/${year_expirationDate}`);

                $(`#country-document-primary-${element_id}`).val(result.country);

                const file = document.getElementById(`imagen-document-${element_id}`).files[0];
                const urlImagen = URL.createObjectURL(file);

                var imgElement = document.getElementById(`imageDocument-${element_id}`);
                imgElement.src = urlImagen;
                imgElement.classList.remove("hidden");
                
            }
            else{
                $(`#number-document-${element_id}`).val(result.document_no);

                const expirationDate = result.date_of_expiry;
                let year_expirationDate = "20" + expirationDate.substring(0, 2);
                var month_expirationDate = expirationDate.substring(2, 4);
                var day_expirationDate = expirationDate.substring(4, 6);
                $(`#expiration-document-${element_id}`).val(`${month_expirationDate}/${day_expirationDate}/${year_expirationDate}`);

                $(`#country-document-${element_id}`).val(result.country);

                const file = document.getElementById(`imagen-document-${element_id}`).files[0];
                const urlImagen = URL.createObjectURL(file);

                var imgElement = document.getElementById(`imageDocument-${element_id}`);
                imgElement.src = urlImagen;
                imgElement.classList.remove("hidden");
            }
        
        }
    }
}

