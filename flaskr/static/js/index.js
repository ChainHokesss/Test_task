$(document).ready(function(){
    counter = 1
    $('#add_form').click(function(){
        new_label = $('#input_form').find($('label')).first().clone()
        new_label.text("name" + counter + ' ');

        new_input = $('#input_form').find($('input')).first().clone()
        new_input.prop("name", 'value'+counter)

        $('#input_form').append(new_label, new_input, '</br>')
        
        counter ++;
    });
});