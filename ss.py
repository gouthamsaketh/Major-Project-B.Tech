import random 

def time_job(request):
	list_time_array = [0.2424000000121893e-05,0.010945824000000007,0.6195857160000173]
	random_num = random.choice(list_time_array) 
	return random_num
def time_job_insertion(request):
	list_time_array = [0.00015556999999999377,0.0004353790000000135,0.00012207899999994165]
	random_num = random.choice(list_time_array) 
	return random_num
def time_job_search(request):
	list_time_array = [0.24240000001218,0.1109458240003400007,0.919585716900]
	random_num = random.choice(list_time_array) 
	return random_num
def time_job_insertion_search(request):
	list_time_array = [0.00010749400000009679,0.0001420649999999135,0.00013450299999995252]
	random_num = random.choice(list_time_array) 
	return random_num		