/**
 * Created by than2613 on 1/12/2016.
 */
function changeRate(number, locationId){
    $.ajax({
        'url': '/location/'+locationId+'/rate',
        'data': {
            'stars': number
        },
        'success': function success(data) {
            updateStars(number);
        },
        'method': 'POST'
    }
    )
}

function updateStars(number){
    $('#star > div').each(function () {
        if (parseInt(this.id.substr(4)) <= number) {
            $(this).addClass("goldstar");
            $(this).removeClass("blackstar");
            $(this).removeClass("silverstar");
        } else {
            $(this).addClass("blackstar");
            $(this).removeClass("goldstar");
            $(this).removeClass("silverstar");
        }
    });
}