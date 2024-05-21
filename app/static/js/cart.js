$(document).ready(function(){
    
    $('.add-to-cart').on('click',function(){
        const idsg = $(this).data('id');
        const titlesg = $(this).data('title');
        const pricesg = $(this).data('price');

        $.post('/a_cart',{
            id:idsg,
            title:titlesg,
            price:pricesg

        }, function(data){
            alert(data.message || `Agregar la canción`);
        });

    });

});