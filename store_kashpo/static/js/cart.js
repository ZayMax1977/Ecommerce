var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		if (this.dataset.color){
		    var color = this.dataset.color
		}else{
		    color  = document.getElementById('color_' + String(productId)).value
		}

		if (user === 'AnonymousUser'){
			console.log('User is not authenticated')

		}else{

			updateUserOrder(productId, action, color)
		}
	})
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
