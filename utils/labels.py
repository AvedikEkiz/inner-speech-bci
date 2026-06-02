import pandas as pd

INFORMATIVE = frozenset({
    'BACK1', 'BACK2', 'DOWN1', 'DOWN2', 'FORWARD1', 'FORWARD2',
    'LEFT1', 'LEFT2', 'NEXT1', 'NEXT2', 'RIGHT1', 'RIGHT2', 'UP1', 'UP2',
})

SERVICE = frozenset({'GO', 'GZ'})

# Subjects whose recording used an alternative paradigm:
# one marker covered multiple repetitions (~1 s epochs cut post-hoc).
ATYPICAL = frozenset({
    ('Russian', 'sub1'),
    ('Russian', 'sub3'),
    ('Russian', 'sub5'),
    ('Russian', 'sub6'),
    ('Russian', 'sub10'),
})

_ROWS = [
    # label     id_ru  id_es   english     russian    spanish        speech_type
    ('BACK1',      1,     1,  'back',    'назад',   'atrás',       'overt'),
    ('BACK2',      2,     2,  'back',    'назад',   'atrás',       'inner'),
    ('DOWN1',      3,     3,  'down',    'вниз',    'abajo',       'overt'),
    ('DOWN2',      4,     4,  'down',    'вниз',    'abajo',       'inner'),
    ('FORWARD1',   5,     5,  'forward', 'вперёд',  'adelante',    'overt'),
    ('FORWARD2',   6,     6,  'forward', 'вперёд',  'adelante',    'inner'),
    ('GO',         7,     7,  'go',      'старт',   'inicio',      'service: block start'),
    ('GZ',         8,     8,  'rest',    'покой',   'descanso',    'service: rest/baseline'),
    ('LEFT1',      9,     9,  'left',    'влево',   'izquierda',   'overt'),
    ('LEFT2',     10,    10,  'left',    'влево',   'izquierda',   'inner'),
    ('NEXT1',     11,  None,  'next',    'дальше',  '—',           'overt (RU only)'),
    ('NEXT2',     12,  None,  'next',    'дальше',  '—',           'inner (RU only)'),
    ('RIGHT1',    13,    11,  'right',   'вправо',  'derecha',     'overt'),
    ('RIGHT2',    14,    12,  'right',   'вправо',  'derecha',     'inner'),
    ('UP1',       15,    13,  'up',      'вверх',   'arriba',      'overt'),
    ('UP2',       16,    14,  'up',      'вверх',   'arriba',      'inner'),
]

LABEL_INFO = pd.DataFrame(
    _ROWS,
    columns=['label', 'id_russian', 'id_spanish', 'english', 'russian', 'spanish', 'speech_type'],
).set_index('label')
