def get_success(request):
	if 'success_message' in request.session:
		success_message = request.session['success_message']
		del request.session['success_message']
		return { 'success_message': success_message }
	else:
		return { 'success_message': False }
	
