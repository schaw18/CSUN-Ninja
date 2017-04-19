		$(document).ready(function() {
			//Variables to check for form validation
			var regFormError = [true, true, true, true, true, true];
			var formError = [true, true];
			
			//Reset form data
			$('#signinForm').trigger("reset");
			$('#regForm').trigger("reset");			
			
			//Disable form buttons until the fields are complete			
			$('#btnDone').attr('disabled', 'disabled');
			$('#btnSignin').attr('disabled', 'disabled');
			
			
			$('body').css('padding-top', $('#navbar').height());
			$('#dpr-button').click(function(){
				$('#dpr-details').show();
			});
			
			$('#schedule-button').click(function(){
				$('#schedule-details').show();
			});
			$('#drag-button').click(function(){
				$('#drag-details').show();
			});	
				
			
			$('#firstName').blur(function(){
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$('#fNameLabel').text('First Name is Required');
					regFormError[0] = true;
					validateRegForm();
				} else {
					$(this).removeClass('form-field-error');
					$('#fNameLabel').text('');
					regFormError[0] = false;
					validateRegForm();
				}			
			});
			
			$('#lastName').blur(function(){
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$('#lNameLabel').text('Last Name is Required');
					regFormError[1] = true;
					validateRegForm();
				} else {
					$(this).removeClass('form-field-error');
					$('#lNameLabel').text('');
					regFormError[1] = false;
					validateRegForm();
				}
			
			});
			
			$('#emailAddress').blur(function(){
				var patt = /^[a-z]+.[a-z]+.[0-9]+/i;				
				
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$('#emailAddressLabel').text('Email is Required');
					regFormError[2] = true;
					validateRegForm();
				} else if(!patt.test($(this).val())) {
					$(this).addClass('form-field-error');
					$('#emailAddressLabel').text('Valid CSUN Email is required');
					regFormError[2] = true;
					validateRegForm();
				} else {
					$(this).removeClass('form-field-error');
					$('#emailAddressLabel').text('');
					regFormError[2] = false;
					validateRegForm();
				}
			
			});
			
			$('#CSUNID').blur(function(){				
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$('#CSUNIDLabel').text('CSUN ID is Required');
					regFormError[3] = true;
					validateRegForm();
				} else {
					$(this).removeClass('form-field-error');
					$('#CSUNIDLabel').text('');
					regFormError[3] = false;
					validateRegForm();
				}
			
			});
			
			$('#password').blur(function(){				
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$('#passwordLabel').text('Password is Required');
					regFormError[4] = true;
					validateRegForm();
				} else if ($(this).val().length < 8){
					$(this).addClass('form-field-error');
					$('#passwordLabel').text('Password must be 8 characters or more');
					regFormError[4] = true;
					validateRegForm();
				} else {
				
					$(this).removeClass('form-field-error');
					$('#passwordLabel').text('');
					regFormError[4] = false;
					validateRegForm();
					
					if ($('#confirmPassword').val() != $(this).val()){
						$('#confirmPassword').addClass('form-field-error');
						$('#confirmPasswordLabel').text('Passwords do not match');
						regFormError[5] = true;
						validateRegForm();
					} else {
						$('#confirmPassword').removeClass('form-field-error');
						$('#confirmPasswordLabel').text('');
						regFormError[5] = false;
						validateRegForm();
					}
					

				}

		
			});
			
			$('#confirmPassword').blur(function(){				
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$('#confirmPasswordLabel').text('You must confirm password');
					regFormError[5] = true;
					validateRegForm();
				} else if ($('#password').val() != $(this).val()){
					$(this).addClass('form-field-error');
					$('#confirmPasswordLabel').text('Passwords do not match');
					regFormError[5] = true;
					validateRegForm();
				} else {
					$(this).removeClass('form-field-error');
					$('#confirmPasswordLabel').text('');
					regFormError[5] = false;
					validateRegForm();
				}			
			});
			
			
			function validateRegForm() {			
				var regFormErrors = 0; 
				for(var i = 0; i < regFormError.length; i++){
					if(regFormError[i] == true){
						regFormErrors = regFormErrors + 1;
					}					
				}
				
				if(regFormErrors > 0){
					$('#btnDone').attr('disabled', 'disabled');
				} else {
					$('#btnDone').removeAttr('disabled');				
				}
			}

			$('#signinEmail').blur(function(){					
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					$(this).attr('placeholder', 'Email is Required');
					formError[0] = true;
					validateForm();
				} else {
					$(this).removeClass('form-field-error');
					formError[0] = false;
					validateForm();
				}
			
			});
			
			$('#signinPassword').keyup(function(){				
				if($(this).val() == ""){
					$(this).addClass('form-field-error');
					formError[1] = true;
					validateForm();
				} else {
					$(this).removeClass('form-field-error');
					formError[1] = false;
					validateForm();
				}			
			});
			
			function validateForm() {			
				var formErrors = 0; 
				for(var i = 0; i < formError.length; i++){
					if(formError[i] == true){
						formErrors = formErrors + 1;
					}					
				}
				
				if(formErrors > 0){
					$('#btnSignin').attr('disabled', 'disabled');
				} else {
					$('#btnSignin').removeAttr('disabled');				
				}
			}
			
			$('#uploadCancel').click(function () {
				$('#uploadDPRForm').trigger("reset");		
			});
			
		$(window).load(function () { 
			$('body').css('padding-top', $('#navbar').height()); 			
		});		
		
		$(window).resize(function () { 
			$('body').css('padding-top', $('#navbar').height());
		});
			
			
	});
		