from collections import Counter
from pprint import pprint

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


class AdTest():

    def __init__(self):
        self.counter_show_original = 0
        self.counter_show_test = 0
        self.counter_click_original = 0
        self.counter_click_test = 0

    def process_transition(self, request):
        value = request.GET.get('ab_test_arg', None)

        if value == 'original':
            self.counter_show_original += 1

        elif value == 'test':
            self.counter_show_test += 1


    def counting_relationships(self):
        if self.counter_click_original != 0:
            self.original_conversion = self.counter_click_original / self.counter_click_original
        else:
            self.original_conversion = 0
            if self.counter_click_test != 0:
                self.test_conversion = self.counter_show_test / self.counter_click_test
            else:
                self.test_conversion = 0
        #
        # if summ == 0:
        #     self.test_conversion = 0
        #     self.original_conversion = 0
        # else:
        #     self.test_conversion = self.counter_show_test / summ
        #     self.original_conversion = self.counter_show_original / summ

    def print_class(self):
        print(f'ORIGINAL = {self.counter_show_original}       TEST = {self.counter_show_test}')
        print('----------------------------------------------')


AD_TEST = AdTest()


def index(request):
        AD_TEST.process_transition(request)
        AD_TEST.print_class()

        return render(None, 'index.html')


def landing(request):
    index(request)

    if request.GET.get('ab_test_arg') == 'original':
        AD_TEST.counter_click_original = AD_TEST.counter_click_original + 1
        return render(request,  'landing.html')
    else:
        AD_TEST.counter_click_test = AD_TEST.counter_click_test + 1
        return render(request,  'landing_alternate.html')


def stats(request):
    AD_TEST.counting_relationships()

    return render(None, 'stats.html', context={
        'test_conversion': AD_TEST.test_conversion,
        'original_conversion': AD_TEST.original_conversion,
    })
