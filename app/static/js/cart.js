$(document).ready(function(){
    
    $('.add-to-cart').on('click',function(){
        const idsg = $(this).data('id');
        const titlesg = $(this).data('title');
        const pricesg = $(this).data('price');

        $.post('/a_cart',{
            id:idsg,
            title:titlesg,
            price:pricesg

        }, function(){
            window.location.href = '//lc_cancion';
            // alert(data.message || `Agregar la canción`);
        });

    });
    $('.delete').on('click',function(){
        const itemId = $(this).data('id');
        console.log(itemId)
        // $.ajax({
        //     type: 'POST',
        //     url: '/d_cart', // La URL de la ruta Flask
        //     data: { id: itemId }, // Pasar el ID como datos de la solicitud
        //     success: function() {
        //         window.location.href = '/cart';
        //     },
        //     // error: function(xhr, status, error) {
        //     //     // Manejar errores si es necesario
        //     //     console.error(error);
        //     // }
        // });
        $.post('/d_cart',{
            id: itemId
            
        }, function(){
            window.location.href = '/cart';
        });

    
    });
});