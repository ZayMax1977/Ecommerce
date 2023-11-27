var updateBtns = document.getElementsByClassName('update-cart')


for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
//console.log('color: ', this.dataset.color)
		if (this.dataset.color){
		    var color = this.dataset.color
		}else{
		    var color  = document.getElementById('color_' + String(productId)).value
		}

		if (user === 'AnonymousUser'){
			addCookieItem(productId, action, color)

		}else{

			updateUserOrder(productId, action, color)
		}
	})
}
function addCookieItem(productId, action, color){
	console.log('User is not authenticated')
	var productId = productId + "_"+color
	if (action == 'add'){

		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}
        cart[productId]['color'] = color

		}else{
			cart[productId]['quantity'] += 1
			cart[productId]['color'] = color
		}
	}
	if (action == 'remove'){
	    console.log('cart[productId]: ',cart[productId])
		cart[productId]['quantity'] -= 1
		cart[productId]['color'] = color

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
    if (action == 'del'){
        console.log('Item should be del')
        delete cart[productId];

	}
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}


function updateUserOrder(productId, action, color){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'


		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'color': color})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
            location.reload()
		});
}

