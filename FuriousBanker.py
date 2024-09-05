# encoding: utf-8

# (c) 2014-2024 Open Risk, all rights reserved
#
# FuriousBanker is licensed under the MIT license a copy of which is included
# in the source distribution of FuriousBanker. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.

import webbrowser

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from ruamel.yaml import YAML

import calculator


class AppConfig:

    def __init__(self):
        self.new_loan_limit = None
        self.profitability = None
        self.concentration = None
        self.profitability_p = None
        self.concentration_p = None
        self.portfolio_size = None
        self.duration = None
        self.time_delta = None
        self.winning_score = None


class FuriousBankerApp(App):
    __version__ = '0.3'

    def build(self):
        self.icon = 'data/FuriousBankerA1.png'
        root = Root()
        return root


# define the main widget as a BoxLayout
class Root(BoxLayout):
    in_yaml = YAML(typ='unsafe')
    inFile = open('configuration.yml', 'r')
    AC = in_yaml.load(inFile)
    inFile.close()

    # initialize new loan properties
    new_loan_el = NumericProperty()
    new_loan_s = NumericProperty()
    new_loan_exp = NumericProperty()

    new_loan_count = NumericProperty(0)
    new_loan_limit = NumericProperty(AC.new_loan_limit)

    # initialize selected loan properties
    selected_loan_id = NumericProperty()
    selected_loan_el = NumericProperty()
    selected_loan_s = NumericProperty()
    selected_loan_exp = NumericProperty()

    # initialize metrics (current values and previous)
    profitability = NumericProperty(AC.profitability)
    concentration = NumericProperty(AC.concentration)
    score = NumericProperty(0)
    exposures = NumericProperty(0)

    profitability_p = NumericProperty(AC.profitability_p)
    concentration_p = NumericProperty(AC.concentration_p)
    score_p = NumericProperty(0)
    exposures_p = NumericProperty(0)

    # initialize colors of metric indicator labels
    score_r = NumericProperty(1)
    score_g = NumericProperty(1)
    score_b = NumericProperty(1)

    concentration_r = NumericProperty(1)
    concentration_g = NumericProperty(1)
    concentration_b = NumericProperty(1)

    profitability_r = NumericProperty(1)
    profitability_g = NumericProperty(1)
    profitability_b = NumericProperty(1)

    # initialize loan portfolio
    portfolio_size = AC.portfolio_size
    portfolio = {}

    # time keeping goodies
    # game duration (300)
    duration = AC.duration
    time_delta = AC.time_delta
    time = NumericProperty(0)

    winning_score = AC.winning_score

    def increment_time(self, dt):
        self.time += dt

    def time_reset(self):
        self.time = 0

    # instantiation of the root widget
    def __init__(self, **kwargs):
        # print('init')
        super(Root, self).__init__(**kwargs)

        Clock.schedule_interval(self.increment_time, self.time_delta)
        Clock.schedule_once(self.show_gameover, self.duration)

        # initialize a portfolio
        size = self.portfolio_size
        self.portfolio = calculator.init(size)
        self.display_portfolio(0)
        # initialize portfolio metrics
        self.profitability = calculator.profit(self.portfolio)
        self.concentration = calculator.risky_hhi(self.portfolio)
        self.score = calculator.score(self.portfolio)
        self.exposures = calculator.exposure(self.portfolio)

        self.profitability_p = self.profitability
        self.concentration_p = self.concentration
        self.exposures_p = self.exposures
        self.score_p = self.score
        self.update_color()

        # initialize the new loan data
        newloan = calculator.newloan()
        self.display_newloan(newloan)

        # initialize the selected loan data
        loan = self.portfolio[0]
        self.set_selected([loan['index'], loan['el'], loan['s'], loan['exp']])

    # execute this when user clicks the restart button
    def reset(self):
        # print('reset')
        self.time = 0
        size = self.portfolio_size
        self.portfolio = calculator.init(size)
        self.display_portfolio(0)
        self.new_loan_count = 0

        newloan = calculator.newloan()
        self.display_newloan(newloan)

        self.profitability = calculator.profit(self.portfolio)
        self.profitability_p = self.profitability

        self.concentration = calculator.risky_hhi(self.portfolio)
        self.concentration_p = self.concentration

        self.exposures = calculator.exposure(self.portfolio)
        self.exposures_p = self.exposures

        self.score = calculator.score(self.portfolio)
        self.score_p = self.score
        self.update_color()

        loan = self.portfolio[0]
        self.set_selected([loan['index'], loan['el'], loan['s'], loan['exp']])
        # restart the clock
        Clock.unschedule(self.show_gameover)
        Clock.schedule_once(self.show_gameover, self.duration)

    # execute this when the user wants to read the full documentation
    def web_docs(self):
        webbrowser.open_new("https://www.openriskmanagement.com/furiousbanker/")

    # execute this when a different loan is selected
    def set_selected(self, selloan):
        # print('set_selected')
        self.selected_loan_id = selloan[0]
        self.selected_loan_el = selloan[1]
        self.selected_loan_s = selloan[2]
        self.selected_loan_exp = selloan[3]

    # execute this when a different loan is selected
    def select_other(self, instance):
        # print('test')
        loanid = self.portfolio[int(instance.ID)]['index']
        el = self.portfolio[int(instance.ID)]['el']
        s = self.portfolio[int(instance.ID)]['s']
        exp = self.portfolio[int(instance.ID)]['exp']
        self.selected_loan_id = loanid
        self.selected_loan_el = el
        self.selected_loan_s = s
        self.selected_loan_exp = exp

    # execute this when there is a request for new loan data
    def display_newloan(self, newloan):
        # print('display_new_loan')
        self.new_loan_el = newloan[0]
        self.new_loan_s = newloan[1]
        self.new_loan_exp = newloan[2]

    def accept(self):
        if self.new_loan_count < self.new_loan_limit:
            self.new_loan_count += 1
            # update and display portfolio
            loanid = int(self.selected_loan_id)
            self.portfolio[loanid]['el'] = self.new_loan_el
            self.portfolio[loanid]['s'] = self.new_loan_s
            self.portfolio[loanid]['exp'] = self.new_loan_exp
            self.display_portfolio(loanid)
            # update selected loan data
            self.selected_loan_el = self.new_loan_el
            self.selected_loan_s = self.new_loan_s
            self.selected_loan_exp = self.new_loan_exp
            # update metrics
            # store current values for comparison
            self.profitability_p = self.profitability
            self.concentration_p = self.concentration
            self.score_p = self.score
            self.exposures_p = self.exposures

            self.profitability = calculator.profit(self.portfolio)
            self.concentration = calculator.risky_hhi(self.portfolio)
            self.score = calculator.score(self.portfolio)
            self.exposures = calculator.exposure(self.portfolio)

            self.update_color()

            # initialize new loan data
            newloan = calculator.newloan()
            self.display_newloan(newloan)

    def reject(self):
        # initialize new loan data
        if self.new_loan_count < self.new_loan_limit:
            self.new_loan_count += 1
            newloan = calculator.newloan()
            self.display_newloan(newloan)

    def update_color(self):

        if self.score > self.score_p:
            self.score_r = 0.3
            self.score_g = 0.7
            self.score_b = 0.3
        elif self.score < self.score_p:
            self.score_r = 0.7
            self.score_g = 0.3
            self.score_b = 0.3
        else:
            self.score_r = 0.6
            self.score_g = 0.6
            self.score_b = 0.6

        if self.concentration < self.concentration_p:
            self.concentration_r = 0.3
            self.concentration_g = 0.7
            self.concentration_b = 0.3
        elif self.concentration > self.concentration_p:
            self.concentration_r = 0.7
            self.concentration_g = 0.3
            self.concentration_b = 0.3
        else:
            self.concentration_r = 0.6
            self.concentration_g = 0.6
            self.concentration_b = 0.6

        if self.profitability > self.profitability_p:
            self.profitability_r = 0.3
            self.profitability_g = 0.7
            self.profitability_b = 0.3
        elif self.profitability < self.profitability_p:
            self.profitability_r = 0.7
            self.profitability_g = 0.3
            self.profitability_b = 0.3
        else:
            self.profitability_r = 0.6
            self.profitability_g = 0.6
            self.profitability_b = 0.6

    #
    # execute this whenever there is a portfolio data refresh event
    #
    def display_portfolio(self, selected_id):
        # clear any previously bound widgets
        self.slayout.clear_widgets()

        for i in range(len(self.portfolio)):
            loanid = self.portfolio[i]['index']
            el = self.portfolio[i]['el']
            s = self.portfolio[i]['s']
            exp = self.portfolio[i]['exp']
            if i == selected_id:
                btn = ToggleButton(size_hint=(exp, 0.05), group='Data', text=str(i + 1), state='down')
                btn.ID = str(i)
            else:
                btn = ToggleButton(size_hint=(exp, 0.05), group='Data', text=str(i + 1))
                btn.ID = str(i)
            self.slayout.add_widget(btn)
            btn.bind(on_press=self.select_other)

    #
    # function to show an About popup
    #
    def about_popup(self):

        about = """
FuriousBanker: [i]The Credit Detox Challenge[/i]. Version 0.3

FuriousBanker is a mobile educational game series developed by Open Risk to enable modern interactive eLearning for people working in or studying financial risk management.  The game concepts and logic are directly derived from realistic concepts and tools used in practice (but may have been simplified and/or dramatized).

[b]Copyright: Open Risk, 2014-2020, All Rights Reserved[/b]

About Open Risk:
Open Risk is an independent provider of training and risk analysis tools to the broader financial services community with a strong focus on openness and standards. Please read more about our mission at the Open Risk website (https://www.openriskmanagement.com)
"""

        btnclose = Button(text='Close', size_hint_y=None, height='30sp')
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(font_size='14sp', markup=True, text_size=(420, None), text=about))
        content.add_widget(btnclose)
        popup = Popup(title='About', content=content, size_hint=(1, 1))
        btnclose.bind(on_release=popup.dismiss)
        popup.open()

    #
    # function to show the instructions popup
    #
    def learn_popup(self):

        objective = """You inherited a pretty toxic portfolio and your objective is to reduce the concentration risk, even while improving your profitability. 
    
You need to detox your portfolio (reach a score of at least 500) within a limited time, or otherwise face rejection and the wrath of the regulators!
   
Good luck FuriousBanker, show the world what you can achieve!"""

        portfolio = """The largest exposures of your current portfolio are shown on the right column. The length of the bars corresponds to exposure size. Maximum exposure is 1 bln. Its a lot of money in most currencies! 
    
To see the details of each large loan simply select it by clicking it. You then get to see this loan's  expected loss, credit spread and precise size in the cyan column.
    
The rest of the portfolio does not contribute to concentration and is not shown. 
"""
        new_loans = """You can see the current new loan proposal on the left (green) column. If you like the new loan you can accept it and thereby replace the currently selected (cyan) loan, which dissapears never to be seen again.
   
Your individual loan size limit is 1 bln, so be careful with that money. Reject the current proposed loan to get a new proposal. You have a limited supply of new loans per season (100) so use them wisely!
"""

        metrics = """The profitability of your portfolio is the difference between what you earn on each loan (the credit spread) and what you expect to lose (on average), your expected loss.  It is shown as percentage of your total portfolio size.
        
The concentration risk measure is based on the HHI index as applied to the expected loss of the loans. Hence a portfolio with large concentrations of expected loss with have a larger index. 

Your game score combines profitability and concentration (it is actually the ratio of the two) so you will need to manage both to achieve your detox targets.  
"""

        btnclose = Button(text='Close', size_hint_y=None, height='30sp')
        content = BoxLayout(orientation='vertical')
        items = Accordion(orientation='horizontal')
        item1 = AccordionItem(title="Metrics")
        item1.add_widget(Label(font_size='16sp', text_size=(420, None), markup=True, text=metrics))
        items.add_widget(item1)
        item1 = AccordionItem(title="New Loans")
        item1.add_widget(Label(font_size='16sp', text_size=(420, None), markup=True, text=new_loans))
        items.add_widget(item1)
        item1 = AccordionItem(title="Portfolio")
        item1.add_widget(Label(font_size='16sp', text_size=(420, None), markup=True, text=portfolio))
        items.add_widget(item1)
        item1 = AccordionItem(title="Objective")
        item1.add_widget(Label(font_size='16sp', text_size=(420, None), markup=True, text=objective))
        items.add_widget(item1)
        content.add_widget(items)
        content.add_widget(btnclose)
        popup = Popup(title='Instructions', content=content, size_hint=(1, 1))
        btnclose.bind(on_release=popup.dismiss)
        popup.open()

    #
    # function to show a Game Over popup
    #
    def show_gameover(self, instance):
        btnclose = Button(text='Restart', size_hint_y=None, height='50sp')
        content = BoxLayout(orientation='vertical')
        # Top label
        content.add_widget(Label(text='You have run out of time!'))
        # Conditional on score
        if self.score > self.winning_score:
            content.add_widget(Image(source='data/FuriousBankerH1.png', pos=(400, 100), size=(256, 256)))
            content.add_widget(Label(text='You managed to detox the portfolio!'))
        else:
            content.add_widget(Image(source='data/FuriousBankerA1.png', pos=(400, 100), size=(256, 256)))
            content.add_widget(Label(text='You failed to detox the portfolio!'))
        # Bottom button
        content.add_widget(btnclose)
        popup = Popup(title='Game Over', content=content, size_hint=(1, 1))
        popup.bind(on_dismiss=self.onclose)
        btnclose.bind(on_release=popup.dismiss)
        popup.open()

    #
    # cleaning up before shutting down
    #
    def onclose(self, instance):
        self.reset()
        # reset the clock
        Clock.unschedule(self.show_gameover)
        Clock.schedule_once(self.show_gameover, self.duration)

    # function to Quit the App
    def exit(self):
        App.get_running_app().stop(self)


if __name__ == '__main__':
    FuriousBankerApp().run()
