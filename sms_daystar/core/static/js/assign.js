
    // Function to handle checkbox change event
    function handleCheckboxChange(checkbox) {
        if (checkbox.checked) {
            // If checkbox is checked, remove the corresponding baby from the list
            var babyId = checkbox.value;
            var babyLabel = document.querySelector('label[for="id_babies_' + babyId + '"]').textContent;
            var select = document.getElementById('id_babies');
            for (var i = 0; i < select.options.length; i++) {
                if (select.options[i].text === babyLabel) {
                    select.remove(i);
                    break;
                }
            }
        }
    }
    
    // Attach event listener to checkboxes
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            handleCheckboxChange(checkbox);
        });
    });