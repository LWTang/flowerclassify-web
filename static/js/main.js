$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#result_extend').hide();
    $('.flower-info').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result-data').text('');
        $('#result').hide();
        $('#result-data1').text('');
        $('#result_extend').hide();

        $('.flower-info').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        //var form_data_extend = new FormData($('#upload-file')[1]);
//        console.log(form_data);

        // Show loading animation
        $(this).hide();
        $('.loader').show();


        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            //data_extend: form_data_extend,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result_extend').fadeIn(600);
                $('#result-data').text(data[0]);
                $('#result-data1').text(data[1]);
                $('.flower-name').text($('#result-data').text());
                $('.baidu').attr('src', `https:\/\/baike.baidu.com\/item\/${$('#result-data').text()}`);
                $('.flower-info').show();
            },
        });

    });

});
