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
    $('.delete').on('click',function(){
        const idc = $(this).data('id');
        console.log(idc)
        // $.post('/d_cart',{
            // id:idc
            
        // }, function(data){
        //     alert(data);
        // });
    });
});