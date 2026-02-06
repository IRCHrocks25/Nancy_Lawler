import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MASTER_DIR = os.path.join(ROOT, 'docs', 'master_copy')

mappings = {
    'hero.txt': 'myApp/templates/myApp/includes/hero.html',
    'whats_happening.txt': 'myApp/templates/myApp/includes/whats_happening.html',
    'hopscotch_effect.txt': 'myApp/templates/myApp/includes/hopscotch_effect.html',
    'why_hard.txt': 'myApp/templates/myApp/includes/why_hard.html',
    'where_operates.txt': 'myApp/templates/myApp/includes/where_operates.html',
    'clarity_to_strategy.txt': 'myApp/templates/myApp/includes/clarity_to_strategy.html',
    'built_for_sports.txt': 'myApp/templates/myApp/includes/built_for_sports.html',
    'who_is_for.txt': 'myApp/templates/myApp/includes/who_is_for.html',
    'outcome.txt': 'myApp/templates/myApp/includes/outcome.html',
    'final_cta.txt': 'myApp/templates/myApp/includes/final_cta.html',
    'footer.txt': 'myApp/templates/myApp/includes/footer.html',
    'orientation.txt': 'myApp/templates/myApp/orientation.html',
    'survey_questions.txt': 'myApp/templates/myApp/survey.html',
    'thank_you.txt': 'myApp/templates/myApp/thank_you.html',
}


def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None


def find_master_lines_in_target(master_text, target_text):
    missing = []
    for i, line in enumerate(master_text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if s in target_text:
            continue
        missing.append((i, line))
    return missing


def main():
    report = []

    for master_file, target_rel in mappings.items():
        master_path = os.path.join(MASTER_DIR, master_file)
        target_path = os.path.join(ROOT, target_rel)

        master_text = load_file(master_path)
        target_text = load_file(target_path)

        if master_text is None:
            report.append((master_file, 'ERROR', f'Master file missing: {master_path}'))
            continue
        if target_text is None:
            report.append((master_file, 'ERROR', f'Target template missing: {target_path}'))
            continue

        missing = find_master_lines_in_target(master_text, target_text)
        if not missing:
            report.append((master_file, 'OK', f'All lines found in {target_rel}'))
        else:
            report.append((master_file, 'MISSING', f'{len(missing)} lines not found in {target_rel}'))
            for lineno, line in missing:
                report.append((master_file, 'MISSING_LINE', f'Line {lineno}: {line}'))

    # Print report
    for item in report:
        print(f'{item[0]:<25} {item[1]:<10} {item[2]}')


if __name__ == '__main__':
    main()
