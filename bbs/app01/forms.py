from django import forms


class Register(forms.Form):
    username = forms.CharField(max_length=16, min_length=6,
                               error_messages={
                                   'required': '用户名不可以为空',
                                   'max_length': '用户名不能超过16位',
                                   'min_length': '用户名至少位6位',
                               },
                               widget=forms.widgets.TextInput(attrs={
                                   'class': 'form-control'
                               }),
                               label='用户名',
                               )
    password = forms.CharField(max_length=16, min_length=6,
                               error_messages={
                                   'required': '密码不可以为空',
                                   'max_length': '密码不能超过16位',
                                   'min_length': '密码至少位6位',
                               },
                               widget=forms.widgets.PasswordInput(attrs={
                                   'class': 'form-control'
                               }),
                               label='密码',
                               )
    re_password = forms.CharField(max_length=16, min_length=6,
                                  error_messages={
                                      'required': '密码不可以为空',
                                      'max_length': '密码不能超过16位',
                                      'min_length': '密码至少位6位',
                                  },
                                  widget=forms.widgets.PasswordInput(attrs={
                                      'class': 'form-control'
                                  }),
                                  label='确认密码',
                                  )

    email = forms.EmailField(error_messages={
        'required': '邮箱不能为空',
        'invalid': '邮箱格式不正确'
    },
        widget=forms.widgets.EmailInput(attrs={
            'class': 'form-control'
        }),
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            self.add_error('re_password', '两次密码不一致')
        return self.cleaned_data
