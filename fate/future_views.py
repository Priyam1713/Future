"""Select readable summaries and plot coordinates from native results."""

from fractions import Fraction


def number(value):
    return float(Fraction(value)) if isinstance(value, str) else float(value)


def percent(value):
    v = number(value) * 100
    return f'{v:.2f}%' if 99.95 < v < 100 or 0 < v < .05 else f'{v:.1f}%'


def series(label, values):
    return dict(label=label, points=[[i, number(v)] for i,v in enumerate(values) if v is not None])


def datum(label, value):
    return dict(label=str(label), value=number(value))


def view(status, title, lead, **instrument):
    return dict(status=status,title=title,lead=lead,instrument=instrument)


def project(i,q,r,private=False):
    if i == 24:
        m = r['metrics']
        return view('Your draft' if private else 'Teaching excerpt', f'{m["words"]} words on the page',
            'The first draft preserves the words in the order they were written.',
            text=r['first_draft']['text'], labels=[row['event']['type'] for row in r['timeline']],
            notes=[rule['statement'] for rule in r['procedure']['rules'][:4]])
    if i == 26:
        v = r['concept_references'][0]['reference']
        return view('Practitioner reference', v['id'].replace('_',' ').title(), v['description'],
            labels=[row['id'].replace('_',' ') for row in r['concept_references']], notes=[v['provenance']['locator'],*r['editorial_questions']])
    if i == 44:
        return view('Simulated chronology', f'{r["pair_counts"]["eligible"]} eligible comparisons',
            'Explore the locked entries and later observations from a completed synthetic ledger.',
            labels=[row['chronology'].replace('_',' ') for row in r['pairs']],
            notes=[', '.join(row['ratings'].values()) or 'No rating' for row in r['pairs']])
    if i == 45:
        v = r['result']
        return view('Declared cue exercise', f'Option {v["selected"]}' if v['selected'] else 'The rule abstains',
            f'The first cue that distinguishes the options is {v["decisive_cue"]}.' if v['selected'] else 'The declared cues leave the choice open.',
            labels=[row['cue']['cue_id'] for row in v['inspected']],
            notes=[(' · '.join(row['cue']['values'])) + (' · decisive' if row['discriminates'] else ' · skipped') for row in v['inspected']])
    if i == 46:
        v = r['result']['compatibility']
        titles = {'episodic_like_compatible':'Specific dream recollection', 'familiarity_like_compatible':'Dream familiarity',
                  'dreamy_state_compatible':'Present dream-like state', 'unclassifiable':'Unclassifiable',
                  'review_required':'Needs review', 'unsupported':'Outside the category'}
        return view('Declared experience' if private else 'Synthetic memory example', titles.get(v['status'],v['status']),
            'The category follows the features declared for this recollection.',
            labels=['Experience','Record','Annotation'], notes=[v['qualification']])
    if i == 49:
        body = r['result']
        if q['task']=='benchmark':
            e = body['evaluation']
            return view('Retrospective NOAA evaluation', e['selection']['selected'].title() + ' selected',
                'The native benchmark selects on validation error and reports the held-out test separately.',
                bars=[datum(x['model'],x['macro_mae']['exact']) for x in e['summary']['validation']],
                notes=[e['vintage']])
        observed = [row['value'] for row in body['dataset']['series'][0]['observations']]
        predicted = [c['prediction']['exact'] for c in body['cells']]
        name = q['model'].split('_')[0].upper() if q['model'].startswith('ses_') else q['model'].title()
        return view('Synthetic monthly series', f'{name} · {number(predicted[0]):.2f}',
            'The first point estimate uses the four observed months. The dashed trace shows the next three native estimates.',
            series=[series('Observed',observed),series('Model',([None]*(len(observed)-1))+[observed[-1]]+predicted)],
            labels=[row['period'] for row in body['dataset']['series'][0]['observations']]+[c['target_period'] for c in body['cells']])
    if i == 50:
        states = r['result']['statevector']
        count = len(q['circuit']['gates'])
        return view('Ideal circuit simulation', f'{count} {"gate" if count==1 else "gates"} · {len(states)} outcomes',
            'The bars show the native terminal bitstring probabilities for the selected two-wire circuit.',
            bars=[datum(s['bitstring'],s['probability']) for s in states], gates=q['circuit']['gates'])
    if i == 51:
        ledger = r['result']['ledger']
        before, after = (row['record']['probability'] for row in ledger['actions'][:2])
        return view('Synthetic probability update', f'{percent(before)} → {percent(after)}',
            'The native ledger applies your chosen likelihood ratio to the existing prior. The outcome remains unresolved.',
            bars=[datum('Prior',before),datum('Updated',after)], labels=['Recorded prior','Evidence update','Unresolved event'])
    if i == 52:
        scenario = r['scenarios'][0]['rows'][0]
        return view('Synthetic threshold network', f'{scenario["final_active"]} active at the last round',
            'One selected starting node can activate its neighbours according to the declared thresholds.',
            labels=q['population']['nodes'], links=q['scenarios'][0]['edges'], frames=scenario['states'],
            notes=['Thresholds: ' + ', '.join(row['node']+' · '+row['phi'] for row in q['scenarios'][0]['thresholds'])])
    if i == 53:
        final = r['final_posterior']
        return view('Synthetic sensor twin', f'{number(final["mean"]):.2f} V estimated state',
            'The native filter updates when a measurement is available. An empty point leaves the instrument in prediction-only mode.',
            series=[series('Measurement',[row['value'] for row in r['rows']]),
                    series('Filtered state',[row['posterior_mean'] for row in r['rows']]),
                    series('Open loop',[row['open_loop_mean'] for row in r['rows']])],
            labels=[f'Tick {row["tick"]} · {row["correction"]}' for row in r['rows']])
    if i == 54:
        s = r['scenarios'][0]
        return view('Cellular automaton', f'{s["final_alive"]} living cells after {q["ticks"]} generations',
            'Each frame is a native synchronous update using the same initial grid and a zero exterior.',
            frames=[sum(row,[]) for row in s['state_trace']], counts=[row['alive'] for row in s['counts']])
    if i == 55:
        latest = r['predictions'][-1]
        return view('Offline synthetic features', f'Nearest centroid · Class {latest["prediction"]}',
            'The native classifier compares the selected held-out feature vector with two fixed training centroids.',
            points=[dict(label=k,xy=[number(v[0]),number(v[1])]) for k,v in r['centroids'].items()]+[
                dict(label='Held-out vector',xy=[number(z) for z in r['features'][latest['id']][:2]])],
            bars=[datum(k,v) for k,v in latest['distances'].items()])
    if i == 56:
        risks = r['interventional']
        value = risks['contrast_last_minus_first'] if risks else None
        return view('Synthetic causal model', f'Adjusted difference · {percent(value)}' if value is not None else 'Intervention unavailable',
            'Native identification depends on the declared graph and adjustment set. Observed association remains available.',
            labels=[n['id'] for n in q['nodes']], links=q['edges'], bars=[datum(k,v) for k,v in (risks or r['observational'])['risks'].items()])
    if i == 57:
        v = r['questions']['q1']
        return view('Synthetic forecast pool', f'{percent(v["probability"])} pooled probability',
            'The native pool combines the two synthetic forecasters with equal weights.',
            bars=[datum('Forecaster '+k.upper(),v) for k,v in v['selected_probabilities'].items()]+[datum('Pool',v['probability'])])
    if i == 58:
        v = r['final']
        return view('Play-credit market', f'{percent(v["modeled_prices"]["YES"])} model price for Yes',
            f'The synthetic trader holds {v["q"]["YES"]} Yes shares. Charges and prices are computed by the pinned cost function.',
            bars=[datum(k,v) for k,v in v['modeled_prices'].items()],
            notes=[f'Cumulative play-credit charge: {number(v["net_charges"]):.2f}'])
    if i == 59:
        rows = r['rows']
        return view('Synthetic Lorenz trajectories', f'{rows[-1]["refined_separation"]:.3f} final separation',
            'Two nearly identical starts follow the same equations. The instrument plots the native refined trajectories.',
            series=[dict(label=label,points=[[row[field][0],row[field][2]] for row in rows])
                    for label,field in [('Original','refined_base'),('Perturbed','refined_perturbed')]],
            counts=[row['refined_separation'] for row in rows], labels=[row['time'] for row in rows])
    return view('Hypothetical scenario tree', f'{number(r["expected_utility"]):.2f} expected utility',
        'Weights and outcomes describe the configured scenario. Each node shows its native accumulated branch mass.',
        nodes=[dict(id=n['id'],parent=n['parent'],mass=n['mass'],depth=n['depth'],utility=n['declared_utility']) for n in r['nodes']],
        notes=[f'Leaf mass: {r["total_leaf_mass"]}'])
