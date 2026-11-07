import copy,math,unittest
from decimal import Decimal as D,localcontext,Inexact
from fractions import Fraction as F
from future.prediction_markets import read,cost_prices
from scripts.verify_prediction_markets import fixture,check_case,numeric_checks,verify_report
class PredictionMarketTests(unittest.TestCase):
    def test_numerical_and_series_references(self):numeric_checks()
    def test_fixed_decimal_context(self):
        q=fixture()['cases']['buy-one']['input'];expected=read(q)
        with localcontext() as ctx:
            ctx.prec=6;ctx.traps[Inexact]=True;actual=read(q)
        self.assertEqual(expected,actual)
    def test_quote_never_executes(self):
        r=read(fixture()['cases']['quote-only']['input']);self.assertEqual(r['initial'],r['trace'][0]['financial_after']);self.assertEqual(r['final']['executed_trades'],0);self.assertEqual(r['ledger'],[])
    def test_isolated_budget_refusal(self):
        r=read(fixture()['cases']['budget']['input']);self.assertEqual(r['quotes'][0]['receipt']['feasibility_reasons'],['insufficient_credit']);self.assertEqual(r['trace'][1]['reason'],'insufficient_credit');self.assertEqual(r['initial'],r['trace'][-1]['financial_after'])
    def test_isolated_short_refusal(self):
        r=read(fixture()['cases']['naked-short']['input']);self.assertEqual(r['quotes'][1]['receipt']['feasibility_reasons'],['insufficient_position']);self.assertEqual(r['trace'][-1]['reason'],'insufficient_position');self.assertEqual(r['final']['executed_trades'],1)
    def test_idempotent_after_settlement(self):
        r=read(fixture()['cases']['idempotent-after-settlement']['input']);self.assertEqual(len(r['ledger']),2);self.assertEqual(r['counters']['idempotent_replays'],1);self.assertEqual(r['final']['settlements'],1)
    def test_roundtrip_exact_grid(self):
        r=read(fixture()['cases']['reverse']['input']);self.assertEqual(r['initial'],r['trace'][-1]['financial_after']);self.assertEqual(sum(map(F,r['final']['charges']),F(0)),0);self.assertEqual(r['final']['economic_revision'],2)
    def test_yes_no_symmetry(self):
        q=copy.deepcopy(fixture()['cases']['buy-one']['input']);base=read(q);q['events'][0]['outcome']='NO';other=read(q)
        self.assertEqual(base['final']['charges'],other['final']['charges']);self.assertEqual(base['final']['modeled_prices']['YES'],other['final']['modeled_prices']['NO'])
    def test_balanced_other_settlement(self):
        q=copy.deepcopy(fixture()['cases']['balanced-settlement']['input']);q['events'][-1]['outcome']='NO';r=read(q);self.assertEqual(r['final']['realized_maker_profit'],'0');self.assertEqual(r['final']['total_payout'],'1');verify_report(r)
    def test_strict_close_boundary(self):
        r=read(fixture()['cases']['execute-at-cutoff']['input']);self.assertEqual(r['trace'][-1]['reason'],'market_closed');self.assertEqual(r['final']['net_charges'],'0')
    def test_settled_positions_are_history(self):
        r=read(fixture()['cases']['settle-yes']['input']);self.assertEqual(r['final']['accounts']['alice']['positions']['YES'],'1');self.assertEqual(r['final']['remaining_payout_liability'],'0');self.assertTrue(r['final']['settled'])
    def test_extreme_float_negative_control(self):
        with self.assertRaises(OverflowError):math.exp(1000)
        r=cost_prices({'YES':D(1000),'NO':D(0)},D(1));self.assertGreater(r['prices']['NO'],0);self.assertLessEqual(abs(sum(map(F,r['prices'].values()),F(0))-1),F(1,10**60))
def make_case(c):
    def test(self):check_case(c)
    return test
for name,c in fixture()['cases'].items():setattr(PredictionMarketTests,'test_fixture_'+name.replace('-','_'),make_case(c))
if __name__=='__main__':unittest.main()
