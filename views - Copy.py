from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime, timedelta
from datetime import date 
import datetime
def register(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('mail')
		uname = request.POST.get('username')
		psw = request.POST.get('password')
		pnum = request.POST.get('num')
		country = request.POST.get('country')
		state = request.POST.get('state')
		city = request.POST.get('city')
		addr = request.POST.get('addr')
		user_exist = User_Detail.objects.filter(username=uname)
		phone = len(pnum)
		if user_exist:
			messages.success(request,'Username Already Exist.')
		else:
			if phone == 10:
				crt = User_Detail.objects.create(name=name,email=email,
				phone_number=pnum,username=uname,password=psw,
				country=country,state=state,city=city,address=addr)
				if crt:
					messages.success(request,'Registered Successfully')
			else:
				messages.success(request,'Phone Number Must Contain 10 Digit')
	return render(request,'register.html',{})
def user_login(request):
	if request.session.has_key('user'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('uname')
			password =  request.POST.get('psw')
			post = User_Detail.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('uname')
				request.session['user'] = username
				a = request.session['user']
				sess = User_Detail.objects.only('id').get(username=a).id
				request.session['user_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'login.html',{})
def dashboard(request):
	if request.session.has_key('user'):
		return render(request,'dashboard.html',{})
	else:
		return render(request,'login.html',{})
def logout(request):
	try:
		del request.session['user']
		del request.session['user_id']
	except:
		pass
	return render(request, 'login.html', {})
def admin_login(request):
	if request.session.has_key('admin'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('uname')
			password =  request.POST.get('psw')
			post = Admin_Detail.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('uname')
				request.session['admin'] = username
				a = request.session['admin']
				sess = Admin_Detail.objects.only('id').get(username=a).id
				request.session['admin_id']=sess
				return redirect("admin_dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'admin_login.html',{})
def admin_dashboard(request):
	if request.session.has_key('admin'):
		return render(request,'admin_dashboard.html',{})
	else:
		return render(request,'admin_login.html',{})
def admin_logout(request):
	try:
		del request.session['admin']
		del request.session['admin_id']
	except:
		pass
	return render(request, 'admin_login.html', {})
def add_job(request):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		if request.method == 'POST':
			job_title = request.POST.get('job_title')
			position = request.POST.get('position')
			experience = request.POST.get('experience')
			salary = request.POST.get('salary')
			qualification = request.POST.get('qualification')
			description = request.POST.get('description')
			company_id = Admin_Detail.objects.get(id=int(user_id))
			status = request.POST.get('status')
			company_name = request.POST.get('company_name')
			crt = Job_Detail.objects.create(user_id=company_id,job_title=job_title,position=position,
			experience=experience,salary=salary,qualification=qualification,description=description,
			status=status,company_name=company_name)
			if crt:
				messages.success(request,'Added Successfully')
		return render(request,'add_job.html',{})
	else:
		return render(request,'admin_login.html',{})
def jobs(request):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		detail = Job_Detail.objects.filter(user_id=int(user_id))
		return render(request,'jobs.html',{'detail':detail})
	else:
		return render(request,'admin_login.html',{})
def edit_job(request,pk):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		detail = Job_Detail.objects.filter(id=pk)
		if request.method == 'POST':
			job_title = request.POST.get('job_title')
			position = request.POST.get('position')
			experience = request.POST.get('experience')
			salary = request.POST.get('salary')
			qualification = request.POST.get('qualification')
			description = request.POST.get('description')
			company_name = request.POST.get('company_name')
			status = request.POST.get('status')
			crt = Job_Detail.objects.filter(id=pk).update(company_name=company_name,job_title=job_title,position=position,
			experience=experience,salary=salary,qualification=qualification,description=description,status=status)
			if crt:
				messages.success(request,'Updated Successfully')
		return render(request,'edit_job.html',{'detail':detail})
	else:
		return render(request,'admin_login.html',{})
def delete_job(request,pk):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		detail = Job_Detail.objects.filter(id=pk).delete()
		return redirect('jobs')
	else:
		return render(request,'admin_login.html',{})
def job_details(request):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		detail = Job_Detail.objects.filter(status='Open')
		if request.method == 'POST':
			a = request.POST.get('search')
			detail = Job_Detail.objects.filter(Q(job_title__istartswith=a) | Q(job_title__iendswith=a),status='Open')
			return render(request,'job_details.html',{'detail':detail})
		return render(request,'job_details.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def Applied(request):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		return render(request,'Applied.html',{})
	else:
		return render(request,'login.html',{})
def apply(request,pk):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		uid = User_Detail.objects.get(id=int(user_id))
		job_id = Job_Detail.objects.get(id=pk)
		today = datetime.datetime.now()
		a = today.day
		b = today.year
		c = today.month
		already_applied = Apply_Job.objects.filter(user_id=int(user_id),applied_date=datetime.date(b, c, a))
		if already_applied:
			return redirect('Applied')
			messages.success(request,'Today You Already Applied to the Job.')
		else:
			if request.method == 'POST':
				position = request.POST.get('position')
				salary = request.POST.get('salary')
				date = request.POST.get('date')
				availability = request.POST.get('availability')
				name = request.POST.get('name')
				passport = request.POST.get('passport')
				address = request.POST.get('address')
				postcode = request.POST.get('postcode')
				email = request.POST.get('email')
				phone = request.POST.get('phone')
				dob = request.POST.get('dob')
				gender = request.POST.get('gender')
				q1 = request.POST.get('q1')
				i1 = request.POST.get('i1')
				m1 = request.POST.get('m1')
				g1 = request.POST.get('g1')
				y1 = request.POST.get('y1')
				q2 = request.POST.get('q2')
				i2 = request.POST.get('i2')
				m2 = request.POST.get('m2')
				g2 = request.POST.get('g2')
				y2 = request.POST.get('y2')
				q3 = request.POST.get('q3')
				i3 = request.POST.get('i3')
				m3 = request.POST.get('m3')
				g3 = request.POST.get('g3')
				y3 = request.POST.get('y3')
				q4 = request.POST.get('q4')
				i4 = request.POST.get('i4')
				m4 = request.POST.get('m4')
				g4 = request.POST.get('g4')
				y4 = request.POST.get('y4')
				q5 = request.POST.get('q5')
				i5 = request.POST.get('i5')
				m5 = request.POST.get('m5')
				g5 = request.POST.get('g5')
				y5 = request.POST.get('y5')
				company = request.POST.get('company')
				industry = request.POST.get('industry')
				position_company = request.POST.get('position_company')
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				level = request.POST.get('level')
				monthly_salary = request.POST.get('monthly_salary')
				company1 = request.POST.get('company1')
				industry1 = request.POST.get('industry1')
				position_company1 = request.POST.get('position_company1')
				from1 = request.POST.get('from1')
				todate1 = request.POST.get('todate1')
				level1 = request.POST.get('level1')
				monthly_salary1 = request.POST.get('monthly_salary1')
				company2 = request.POST.get('company2')
				industry2 = request.POST.get('industry2')
				position_company2 = request.POST.get('position_company2')
				from2 = request.POST.get('from2')
				todate2 = request.POST.get('todate2')
				level2 = request.POST.get('level2')
				monthly_salary2 = request.POST.get('monthly_salary2')
				n1 = request.POST.get('n1')
				n2 = request.POST.get('n2')
				ocu1 = request.POST.get('ocu1')
				ocu2 = request.POST.get('ocu2')
				com1 = request.POST.get('com1')
				com2 = request.POST.get('com2')
				contact1 = request.POST.get('contact1')
				contact2 = request.POST.get('contact2')
				mail1 = request.POST.get('mail1')
				mail2 = request.POST.get('mail2')
				ref1 = request.POST.get('ref1')
				ref2 = request.POST.get('ref2')
				crt = Apply_Job.objects.create(user_id=uid,job_id=job_id,position=position,salary=salary,date=date,availability=availability,
				name=name,passport=passport,address=address,postcode=postcode,email=email,phone=phone,
				dob=dob,gender=gender,q1=q1,i1=i1,m1=m1,g1=g1,y1=y1,q2=q2,i2=i2,m2=m2,g2=g2,y2=y2,q3=q3,i3=i3,m3=m3,g3=g3,y3=y3,
				q4=q4,i4=i4,m4=m4,g4=g4,y4=y4,q5=q5,i5=i5,m5=m5,g5=g5,y5=y5,company=company,industry=industry,
				position_company=position_company,fromdate=fromdate,todate=todate,level=level,monthly_salary=monthly_salary,
				company1=company1,industry1=industry1,position_company1=position_company1,from1=from1,todate1=todate1,level1=level1,monthly_salary1=monthly_salary1,
				company2=company2,industry2=industry2,position_company2=position_company2,from2=from2,todate2=todate2,level2=level2,monthly_salary2=monthly_salary2,
				n1=n1,n2=n2,ocu1=ocu1,ocu2=ocu2,com1=com1,com2=com2,contact1=contact1,contact2=contact2,
				mail1=mail1,mail2=mail2,ref1=ref1,ref2=ref2,out_come='Waiting')
				if crt:
					messages.success(request,'Job Applied Successfully')
		return render(request,'apply.html',{})
	else:
		return render(request,'login.html',{})
def applied_job_details(request):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		detail = Apply_Job.objects.filter(user_id=int(user_id))
		return render(request,'applied_job_details.html',{'detail':detail,'user_id':user_id})
	else:
		return render(request,'login.html',{})
def admin_applied_job_details(request):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		detail = Apply_Job.objects.all()
		return render(request,'admin_applied_job_details.html',{'detail':detail})
	else:
		return render(request,'admin_login.html',{})
def applicant(request,pk):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		detail = Apply_Job.objects.filter(id=pk)
		return render(request,'applicant.html',{'detail':detail})
	else:
		return render(request,'admin_login.html',{})
def send_status(request):
	return render(request,'send_status.html',{})	
def shortlist(request,pk,job_id,user_id):
	if request.session.has_key('admin'):
		admin_ids = request.session['admin_id']
		jid = Job_Detail.objects.get(id=job_id)
		aid = Apply_Job.objects.get(id=pk)
		uid = User_Detail.objects.get(id=user_id)
		already_send = Job_Status.objects.filter(user_id=user_id,job_id=job_id,apply_id=pk)
		if already_send:
			return redirect('send_status')
		else:
			if request.method == 'POST':
				date_recceived = request.POST.get('date_recceived')
				hr_officer = request.POST.get('hr_officer')
				out_come = request.POST.get('out_come')
				reason = request.POST.get('reason')
				date = request.POST.get('date')
				Apply_Job.objects.filter(id=pk).update(out_come=out_come)
				crt = Job_Status.objects.create(user_id=uid,job_id=jid,apply_id=aid,date_recceived=date_recceived,hr_officer=hr_officer,
				out_come=out_come,reason=reason,date=date)
				if crt:
					messages.success(request,'Job Status Send.')
		return render(request,'shortlist.html',{})
	else:
		return render(request,'admin_login.html',{})
def check_status(request):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		detail = Job_Status.objects.all()
		return render(request,'check_status.html',{'detail':detail})
	else:
		return render(request,'admin_login.html',{})
def user_check_status(request):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		detail = Job_Status.objects.filter(user_id=int(user_id))
		return render(request,'user_check_status.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def search(request):
	if request.session.has_key('admin'):
		user_id = request.session['admin_id']
		if request.method == 'POST':
			a = request.POST.get('search')
			b = request.POST.get('order_job')
			string = a.replace("+","")
			list_num = []
			if b == 'ASE':
				cursor = connection.cursor()
				sql = '''SELECT d.job_title,d.position,j.name,j.email,s.date_recceived,s.hr_officer,
				s.out_come,s.reason,s.date from app_apply_job as j INNER JOIN app_job_status as s ON
				j.id=s.apply_id_id INNER JOIN app_job_detail as d ON s.job_id_id=d.id 
				where s.out_come='%s' ORDER BY j.name ASC''' % (string)
				post = cursor.execute(sql)
				row = cursor.fetchall()
				length = len(row)
				for i in range(0,length):
					list_num.append(row[i])
				return render(request,'search.html',{'row':row,'string':string,'b':b,'list_num':list_num})
			elif b == 'DESC':
				cursor = connection.cursor()
				sql = '''SELECT d.job_title,d.position,j.name,j.email,s.date_recceived,s.hr_officer,
				s.out_come,s.reason,s.date from app_apply_job as j INNER JOIN app_job_status as s ON
				j.id=s.apply_id_id INNER JOIN app_job_detail as d ON s.job_id_id=d.id 
				where s.out_come='%s' ORDER BY j.name DESC''' % (string)
				post = cursor.execute(sql)
				row = cursor.fetchall()
				return render(request,'search.html',{'row':row,'string':string,'b':b})
		return render(request,'search.html',{})
	else:
		return render(request,'admin_login.html',{})