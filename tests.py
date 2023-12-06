import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from settings import valid_number, valid_email, valid_password

#проверка на наличие 4х основных вкладок для авторизации
def test_auth_tabs(selenium):

    assert selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]').is_displayed()
    assert selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]').is_displayed()
    assert selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-ls"]').is_displayed()
    assert selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-login"]').is_displayed()

#проверка на наличие форм для ввода логина и пароля на всех 4х вкладках
def test_auth_inputs(selenium):

    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    assert selenium.find_element(By.CLASS_NAME, 'rt-input__input-value')
    time.sleep(1)
    mail = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail.click()
    assert selenium.find_element(By.CLASS_NAME, 'rt-input__input-value')
    time.sleep(1)
    ls = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-ls"]')
    ls.click()
    assert selenium.find_element(By.CLASS_NAME, 'rt-input__input-value')
    time.sleep(1)
    login = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-login"]')
    login.click()
    assert selenium.find_element(By.CLASS_NAME, 'rt-input__input-value')
    time.sleep(1)

#проверка на автоматическое переключение на одноименную вкладку, в зависимости от вводимых данных в поле для логина
def test_auto_tab_switch(selenium):

    mail = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail.click()
    time.sleep(1)
    mail_field = selenium.find_element(By.ID, 'username')
    mail_field.send_keys("+79602492414")
    time.sleep(1)
    assert selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')

    ls = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-ls"]')
    ls.click()
    time.sleep(1)
    ls_field = selenium.find_element(By.ID, 'username')
    ls_field.send_keys("+79602492414")
    time.sleep(1)
    assert selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')

    login = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-login"]')
    login.click()
    time.sleep(1)
    login_field = selenium.find_element(By.ID, 'username')
    login_field.send_keys("+79602492414")
    assert selenium.find_element(By.CLASS_NAME, 'rt-input__input-value')
    time.sleep(1)

#проверка на возникновение сообщения об ошибке в случае ввода неверного логина или пароля
def test_incorrect_auth(selenium):

    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    login = selenium.find_element(By.ID, 'username')
    password = selenium.find_element(By.ID, 'password')
    enter = selenium.find_element(By.ID, 'kc-login')
    login.send_keys('valid_number')
    password.send_keys(valid_password)
    enter.click()
  
    assert selenium.find_element(By.ID, 'form-error-message')

#позитивный тест на успешную авторизацию по телефону и паролю
def test_valid_auth(selenium):
    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    login = selenium.find_element(By.ID, 'username')
    password = selenium.find_element(By.ID, 'password')
    enter = selenium.find_element(By.ID, 'kc-login')
    login.send_keys(valid_number)
    password.send_keys(valid_password)
    enter.click()

    assert EC.url_changes('https://b2c.passport.rt.ru/account_b2c')

#позитивный тест на успешную авторизацию по почте и паролю
def test_valid_auth_mail(selenium):
    mail = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail.click()
    login = selenium.find_element(By.ID, 'username')
    password = selenium.find_element(By.ID, 'password')
    enter = selenium.find_element(By.ID, 'kc-login')
    login.send_keys(valid_email)
    password.send_keys(valid_password)
    enter.click()
    assert EC.url_changes('https://b2c.passport.rt.ru/account_b2c')

#тест на автоматический выбор вкладки авторизации по телефону
def test_num_tab_selected(selenium):
    assert EC.element_located_to_be_selected([By.XPATH, '//*[@id="t-btn-tab-phone"]'])

#негативный тест на недопустимость ввода телефона некорректного формата
def test_invalid_num(selenium):
    login = selenium.find_element(By.ID, 'username')
    login.send_keys("+15193074701")
    time.sleep(1)
    assert EC.Alert 

#негативный тест на недопучстимость ввода текста, превышающего длину в 50 символов в поле для e-mail
def test_long_email_input(selenium):
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    # Ввод текста длиной 220 символов
    email_field = selenium.find_element(By.ID, 'username')
    long_text = 'a' * 220
    email_field.send_keys(long_text)
    standart_length = 50

    # Проверка, что введенный текст не соответствует ожидаемому
    if len(email_field.get_attribute('value')) > standart_length:
        assert Exception

#проверка на смену цвета ссылки "забыл пароль" при вводе неверных данных
def test_color_change_of_forgot_password(selenium):
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    forgot_password_link = selenium.find_element(By.ID, 'forgot_password')
    color_before = forgot_password_link.value_of_css_property('color')

    # Ввод неверных данных для вызова ошибки
    username_field = selenium.find_element(By.ID, 'username')
    password_field = selenium.find_element(By.ID, 'password')
    enter_button = selenium.find_element(By.ID, 'kc-login')

    username_field.send_keys('invalid_username')
    password_field.send_keys('invalid_password')
    enter_button.click()

    # Ожидание ошибки
    WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.ID, 'form-error-message'))
    )
    forgot_password_link = selenium.find_element(By.ID, 'forgot_password')
    color_after = forgot_password_link.value_of_css_property('color')

    assert color_before != color_after

#негативный тест на возникновение подсказки при вводе более 12 цифр в поле для ввода логина
def test_12num_symbols_in_fields(selenium):
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys('1234567890123')
    acceptable_digit_length = 12
    if username_field.get_attribute('value') is int and len(username_field.get_attribute('value')) > acceptable_digit_length:
        assert Exception

#тест на отработку сценария в случае, если пользователь забыл пароль
def test_forgot_password(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )

    assert EC.presence_of_all_elements_located([
        (By.ID, 't-btn-tab-phone'),
        (By.ID, 't-btn-tab-mail'),
        (By.ID, 't-btn-tab-login'),
        (By.ID, 't-btn-tab-ls'),
        (By.ID, 'username'),
        (By.ID, 'captcha'),
        (By.ID, 'reset'),
        (By.ID, 'reset-back')
    ])

#тест на присутствие всех необходимых элментов на форме меню, возникающем если нажать на ссылку "забыл пароль"
def test_reset_menu(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_email)

    #ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    assert EC.presence_of_all_elements_located([
        (By.XPATH, '//*[contains(text(), "По номеру телефона")]'),
        (By.XPATH, '//*[contains(text(), "По e-mail")]'),
        (By.XPATH, '//button[@type="submit"][1]'),
        (By.XPATH, '//button[@type="submit"][2]')
    ])

#тест на проверку формы меню, возникающем, если нажать "забыл пароль" и восстановить по почте
def test_reset_by_mail(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_email)

    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )
    
    reset_by_number_radio = WebDriverWait(selenium, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][2]'))
    )
    reset_by_mail_radio.click()

    reset_form_confirm = WebDriverWait(selenium,5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )

    assert EC.presence_of_all_elements_located([
        (By.XPATH, '//button[@name="cancel_reset"]'),
        (By.XPATH, '//button[@class="code-input-container__resend"]'),
    ])
    
#тест на проверку формы меню, возникающем, если нажать "забыл пароль" и восстановить по номеру телефона
def test_reset_by_number(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_number)

    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    reset_by_number_radio = WebDriverWait(selenium, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][1]'))
    )
    reset_by_number_radio.click()

    reset_form_confirm = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )


    assert EC.presence_of_all_elements_located([
        (By.XPATH, '//button[@name="cancel_reset"]'),
        (By.XPATH, '//button[@class="code-input-container__resend"]'),
    ])

#тест на обработку сценария ввода устаревшего кода из смс для восстановления пароля
def test_reset_expired_sms(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_number)
    time.sleep(15)
    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    reset_by_number_radio = WebDriverWait(selenium, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][1]'))
    )
    reset_by_number_radio.click()

    reset_form_confirm = WebDriverWait(selenium, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )

    assert EC.presence_of_element_located((By.ID, 'form-error-message'))

#тест на обработку сценария ввода  кода из смс с буквами, вместо цифр для восстановления пароля
def test_reset_sms_with_letters(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_number)

    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    reset_by_number_radio = WebDriverWait(selenium, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][1]'))
    )
    reset_by_number_radio.click()

    reset_form_confirm = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )

    sms_field = WebDriverWait(selenium, 121).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="rt-sdi-container rt-sdi-container--medium"]')))
    sms_field.send_keys('abcdef')

    assert EC.Alert

#тест на обработку сценария ввода неверного кода из смс для восстановления пароля
def test_reset_sms_wrong_digits(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    phone = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-phone"]')
    phone.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_number)

    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    reset_by_number_radio = WebDriverWait(selenium, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][1]'))
    )
    reset_by_number_radio.click()

    reset_form_confirm = WebDriverWait(selenium, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )

    sms_field = WebDriverWait(selenium, 121).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="rt-sdi-container rt-sdi-container--medium"]')))
    sms_field.send_keys('123456')

    assert EC.Alert

#тест на обработку сценария ввода неверного кода из письма на почту для восстановления пароля
def test_reset_mail_wrong_digits(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_email)

    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    reset_by_mail_radio = WebDriverWait(selenium, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][2]'))
    )
    reset_by_mail_radio.click()

    reset_form_confirm = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )

    mail_field = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="rt-sdi-container rt-sdi-container--medium"]')))
    mail_field.send_keys('123456')

    assert EC.presence_of_element_located((By.ID, 'form-error-message'))

#тест на обработку сценария ввода  кода из письма на почту с буквами, вместо цифр для восстановления пароля
def test_reset_msg_with_letters(selenium):
    forgot_password = selenium.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    reset_form = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container.reset-form-container'))
    )
    mail_tab = selenium.find_element(By.XPATH, '//*[@id="t-btn-tab-mail"]')
    mail_tab.click()
    username_field = selenium.find_element(By.ID, 'username')
    username_field.send_keys(valid_email)
 
    # ручное заполнение капчи

    continue_btn = selenium.find_element(By.ID, 'reset')
    continue_btn.click()

    reset_choice_form = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'card-container__wrapper'))
    )

    reset_by_mail_radio = WebDriverWait(selenium, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//label[@class="rt-radio rt-radio--orange"][2]'))
    )
    reset_by_mail_radio.click()

    reset_form_confirm = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="card-container__wrapper"]'))
    )

    mail_field = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="rt-sdi-container rt-sdi-container--medium"]')))
    mail_field.send_keys('abcdef')

    assert EC.Alert