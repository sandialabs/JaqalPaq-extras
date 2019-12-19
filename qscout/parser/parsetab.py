
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BLOCKCOMMENT COLON EOL FLOAT IDENTIFIER INTEGER LANGLE LBRACE LBRACKET LET LINECOMMENT LOOP MACRO MAP PIPE RANGLE RBRACE RBRACKET REG SEMICOLONprogram : header_statements body_statementsprogram : EOL programheader_statements : header_statement seq_sep header_statementsheader_statements : header_statement \n\t\t\t\t\t\t | header_statement seq_sepheader_statement : register_statement\n\t\t\t\t\t\t| map_statement\n\t\t\t\t\t\t| let_statementregister_statement : REG array_declarationmap_statement : MAP map_target map_sourcemap_target : IDENTIFIERmap_target : array_declarationmap_source : IDENTIFIERmap_target : array_slicelet_statement : LET IDENTIFIER numberbody_statements : body_statement seq_sep body_statementsbody_statements : body_statement\n\t\t\t\t\t   | body_statement seq_sepbody_statement : gate_statement\n\t\t\t\t\t  | macro_definition\n\t\t\t\t\t  | loop_statement\n\t\t\t\t\t  | gate_blockgate_statement : IDENTIFIER gate_arg_listgate_arg_list : gate_arg gate_arg_listgate_arg_list : gate_arg : array_elementgate_arg : IDENTIFIERgate_arg : numbermacro_definition : MACRO IDENTIFIER gate_def_list gate_blockgate_def_list : IDENTIFIER gate_def_listgate_def_list : loop_statement : LOOP let_or_integer gate_blockgate_block : sequential_gate_block\n\t\t\t\t  | parallel_gate_blocksequential_gate_block : LBRACE sequential_statements RBRACEsequential_gate_block : LBRACE EOL sequential_statements RBRACEparallel_gate_block : LANGLE parallel_statements RANGLEparallel_gate_block : LANGLE EOL parallel_statements RANGLEsequential_statements : sequential_statement seq_sep sequential_statementssequential_statements : sequential_statement\n\t\t\t\t\t\t\t | sequential_statement seq_sepsequential_statement : gate_statement\n\t\t\t\t\t\t\t| parallel_gate_block\n\t\t\t\t\t\t\t| loop_statementparallel_statements : parallel_statement par_sep parallel_statementsparallel_statements : parallel_statement\n\t\t\t\t\t\t   | parallel_statement par_sepparallel_statement : gate_statement\n\t\t\t\t\t\t  | sequential_gate_blockarray_declaration : IDENTIFIER LBRACKET let_or_integer RBRACKETarray_element : IDENTIFIER LBRACKET let_or_integer RBRACKETarray_slice : IDENTIFIER LBRACKET slice_indexing RBRACKETslice_indexing : let_or_integerslice_indexing : let_or_integer COLON let_or_integerslice_indexing : let_or_integer COLON let_or_integer COLON let_or_integerlet_or_integer : IDENTIFIER\n\t\t\t\t\t  | INTEGERseq_sep : SEMICOLON\n\t\t\t   | EOL\n\t\t\t   | seq_sep EOLpar_sep : PIPE\n\t\t\t   | EOL\n\t\t\t   | par_sep EOLnumber : INTEGER\n\t\t\t  | FLOAT'
    
_lr_action_items = {'EOL':([0,3,4,5,6,7,12,13,14,15,16,17,20,21,22,23,25,26,27,28,35,36,37,38,39,40,41,42,49,50,51,52,55,56,57,59,61,62,64,67,70,71,73,74,76,77,78,84,85,87,89,90,93,],[3,3,27,-6,-7,-8,27,-19,-20,-21,-22,-25,-33,-34,48,54,59,-58,-59,-9,59,-27,-23,-25,-26,-28,-64,-65,27,-42,-43,-44,78,-48,-49,-60,-10,-13,-15,-24,-32,-35,59,-37,89,-61,-62,-29,-36,-38,-63,-50,-51,]),'REG':([0,3,25,26,27,59,],[8,8,8,-58,-59,-60,]),'MAP':([0,3,25,26,27,59,],[9,9,9,-58,-59,-60,]),'LET':([0,3,25,26,27,59,],[10,10,10,-58,-59,-60,]),'$end':([1,11,12,13,14,15,16,17,20,21,24,26,27,35,36,37,38,39,40,41,42,59,65,67,70,71,74,84,85,87,93,],[0,-1,-17,-19,-20,-21,-22,-25,-33,-34,-2,-58,-59,-18,-27,-23,-25,-26,-28,-64,-65,-60,-16,-24,-32,-35,-37,-29,-36,-38,-51,]),'IDENTIFIER':([2,4,5,6,7,8,9,10,17,18,19,22,23,25,26,27,28,30,31,32,33,35,36,38,39,40,41,42,43,48,54,58,59,60,61,62,63,64,66,68,73,76,77,78,89,90,91,92,93,95,],[17,-4,-6,-7,-8,29,31,34,36,43,45,17,17,-5,-58,-59,-9,62,-11,-12,-14,17,-27,36,-26,-28,-64,-65,68,17,17,-3,-60,45,-10,-13,45,-15,45,68,17,17,-61,-62,-63,-50,45,-52,-51,45,]),'MACRO':([2,4,5,6,7,25,26,27,28,35,41,42,58,59,61,62,64,90,],[18,-4,-6,-7,-8,-5,-58,-59,-9,18,-64,-65,-3,-60,-10,-13,-15,-50,]),'LOOP':([2,4,5,6,7,22,25,26,27,28,35,41,42,48,58,59,61,62,64,73,90,],[19,-4,-6,-7,-8,19,-5,-58,-59,-9,19,-64,-65,19,-3,-60,-10,-13,-15,19,-50,]),'LBRACE':([2,4,5,6,7,23,25,26,27,28,35,41,42,43,44,45,46,54,58,59,61,62,64,68,69,76,77,78,83,89,90,],[22,-4,-6,-7,-8,22,-5,-58,-59,-9,22,-64,-65,-31,22,-56,-57,22,-3,-60,-10,-13,-15,-31,22,22,-61,-62,-30,-63,-50,]),'LANGLE':([2,4,5,6,7,22,25,26,27,28,35,41,42,43,44,45,46,48,58,59,61,62,64,68,69,73,83,90,],[23,-4,-6,-7,-8,23,-5,-58,-59,-9,23,-64,-65,-31,23,-56,-57,23,-3,-60,-10,-13,-15,-31,23,23,-30,-50,]),'SEMICOLON':([4,5,6,7,12,13,14,15,16,17,20,21,28,36,37,38,39,40,41,42,49,50,51,52,61,62,64,67,70,71,74,84,85,87,90,93,],[26,-6,-7,-8,26,-19,-20,-21,-22,-25,-33,-34,-9,-27,-23,-25,-26,-28,-64,-65,26,-42,-43,-44,-10,-13,-15,-24,-32,-35,-37,-29,-36,-38,-50,-51,]),'RBRACE':([17,20,21,26,27,36,37,38,39,40,41,42,47,49,50,51,52,59,67,70,71,72,73,74,85,86,87,93,],[-25,-33,-34,-58,-59,-27,-23,-25,-26,-28,-64,-65,71,-40,-42,-43,-44,-60,-24,-32,-35,85,-41,-37,-36,-39,-38,-51,]),'PIPE':([17,36,37,38,39,40,41,42,55,56,57,67,71,85,93,],[-25,-27,-23,-25,-26,-28,-64,-65,77,-48,-49,-24,-35,-36,-51,]),'RANGLE':([17,36,37,38,39,40,41,42,53,55,56,57,67,71,75,76,77,78,85,88,89,93,],[-25,-27,-23,-25,-26,-28,-64,-65,74,-46,-48,-49,-24,-35,87,-47,-61,-62,-36,-45,-63,-51,]),'INTEGER':([17,19,34,36,38,39,40,41,42,60,63,66,91,93,95,],[41,46,41,-27,41,-26,-28,-64,-65,46,46,46,46,-51,46,]),'FLOAT':([17,34,36,38,39,40,41,42,93,],[42,42,-27,42,-26,-28,-64,-65,-51,]),'LBRACKET':([29,31,36,],[60,63,66,]),'RBRACKET':([45,46,79,80,81,82,94,96,],[-56,-57,90,90,92,93,-54,-55,]),'COLON':([45,46,80,94,],[-56,-57,91,95,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,3,],[1,24,]),'header_statements':([0,3,25,],[2,2,58,]),'header_statement':([0,3,25,],[4,4,4,]),'register_statement':([0,3,25,],[5,5,5,]),'map_statement':([0,3,25,],[6,6,6,]),'let_statement':([0,3,25,],[7,7,7,]),'body_statements':([2,35,],[11,65,]),'body_statement':([2,35,],[12,12,]),'gate_statement':([2,22,23,35,48,54,73,76,],[13,50,56,13,50,56,50,56,]),'macro_definition':([2,35,],[14,14,]),'loop_statement':([2,22,35,48,73,],[15,52,15,52,52,]),'gate_block':([2,35,44,69,],[16,16,70,84,]),'sequential_gate_block':([2,23,35,44,54,69,76,],[20,57,20,20,57,20,57,]),'parallel_gate_block':([2,22,35,44,48,69,73,],[21,51,21,21,51,21,51,]),'seq_sep':([4,12,49,],[25,35,73,]),'array_declaration':([8,9,],[28,32,]),'map_target':([9,],[30,]),'array_slice':([9,],[33,]),'gate_arg_list':([17,38,],[37,67,]),'gate_arg':([17,38,],[38,38,]),'array_element':([17,38,],[39,39,]),'number':([17,34,38,],[40,64,40,]),'let_or_integer':([19,60,63,66,91,95,],[44,79,80,82,94,96,]),'sequential_statements':([22,48,73,],[47,72,86,]),'sequential_statement':([22,48,73,],[49,49,49,]),'parallel_statements':([23,54,76,],[53,75,88,]),'parallel_statement':([23,54,76,],[55,55,55,]),'map_source':([30,],[61,]),'gate_def_list':([43,68,],[69,83,]),'par_sep':([55,],[76,]),'slice_indexing':([63,],[81,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> header_statements body_statements','program',2,'p_program','parser.py',7),
  ('program -> EOL program','program',2,'p_program_blanks','parser.py',57),
  ('header_statements -> header_statement seq_sep header_statements','header_statements',3,'p_header_statements','parser.py',61),
  ('header_statements -> header_statement','header_statements',1,'p_header_statements_s','parser.py',65),
  ('header_statements -> header_statement seq_sep','header_statements',2,'p_header_statements_s','parser.py',66),
  ('header_statement -> register_statement','header_statement',1,'p_header_statement','parser.py',70),
  ('header_statement -> map_statement','header_statement',1,'p_header_statement','parser.py',71),
  ('header_statement -> let_statement','header_statement',1,'p_header_statement','parser.py',72),
  ('register_statement -> REG array_declaration','register_statement',2,'p_register_statement','parser.py',76),
  ('map_statement -> MAP map_target map_source','map_statement',3,'p_map_statement','parser.py',80),
  ('map_target -> IDENTIFIER','map_target',1,'p_map_target_id','parser.py',84),
  ('map_target -> array_declaration','map_target',1,'p_map_target_array','parser.py',88),
  ('map_source -> IDENTIFIER','map_source',1,'p_map_source_id','parser.py',92),
  ('map_target -> array_slice','map_target',1,'p_map_source_array','parser.py',96),
  ('let_statement -> LET IDENTIFIER number','let_statement',3,'p_let_statement','parser.py',100),
  ('body_statements -> body_statement seq_sep body_statements','body_statements',3,'p_body_statements','parser.py',104),
  ('body_statements -> body_statement','body_statements',1,'p_body_statements_s','parser.py',108),
  ('body_statements -> body_statement seq_sep','body_statements',2,'p_body_statements_s','parser.py',109),
  ('body_statement -> gate_statement','body_statement',1,'p_body_statement','parser.py',113),
  ('body_statement -> macro_definition','body_statement',1,'p_body_statement','parser.py',114),
  ('body_statement -> loop_statement','body_statement',1,'p_body_statement','parser.py',115),
  ('body_statement -> gate_block','body_statement',1,'p_body_statement','parser.py',116),
  ('gate_statement -> IDENTIFIER gate_arg_list','gate_statement',2,'p_gate_statement','parser.py',120),
  ('gate_arg_list -> gate_arg gate_arg_list','gate_arg_list',2,'p_gate_arg_list','parser.py',124),
  ('gate_arg_list -> <empty>','gate_arg_list',0,'p_gate_arg_list_empty','parser.py',128),
  ('gate_arg -> array_element','gate_arg',1,'p_gate_arg_array','parser.py',132),
  ('gate_arg -> IDENTIFIER','gate_arg',1,'p_gate_arg_id','parser.py',136),
  ('gate_arg -> number','gate_arg',1,'p_gate_arg_number','parser.py',140),
  ('macro_definition -> MACRO IDENTIFIER gate_def_list gate_block','macro_definition',4,'p_macro_definition','parser.py',144),
  ('gate_def_list -> IDENTIFIER gate_def_list','gate_def_list',2,'p_gate_def_list','parser.py',148),
  ('gate_def_list -> <empty>','gate_def_list',0,'p_gate_def_list_empty','parser.py',152),
  ('loop_statement -> LOOP let_or_integer gate_block','loop_statement',3,'p_loop_statement','parser.py',156),
  ('gate_block -> sequential_gate_block','gate_block',1,'p_gate_block','parser.py',160),
  ('gate_block -> parallel_gate_block','gate_block',1,'p_gate_block','parser.py',161),
  ('sequential_gate_block -> LBRACE sequential_statements RBRACE','sequential_gate_block',3,'p_sequential_gate_block','parser.py',165),
  ('sequential_gate_block -> LBRACE EOL sequential_statements RBRACE','sequential_gate_block',4,'p_sequential_gate_block_blanks','parser.py',169),
  ('parallel_gate_block -> LANGLE parallel_statements RANGLE','parallel_gate_block',3,'p_parallel_gate_block','parser.py',173),
  ('parallel_gate_block -> LANGLE EOL parallel_statements RANGLE','parallel_gate_block',4,'p_parallel_gate_block_blanks','parser.py',177),
  ('sequential_statements -> sequential_statement seq_sep sequential_statements','sequential_statements',3,'p_sequential_statements','parser.py',181),
  ('sequential_statements -> sequential_statement','sequential_statements',1,'p_sequential_statements_s','parser.py',185),
  ('sequential_statements -> sequential_statement seq_sep','sequential_statements',2,'p_sequential_statements_s','parser.py',186),
  ('sequential_statement -> gate_statement','sequential_statement',1,'p_sequential_statement','parser.py',190),
  ('sequential_statement -> parallel_gate_block','sequential_statement',1,'p_sequential_statement','parser.py',191),
  ('sequential_statement -> loop_statement','sequential_statement',1,'p_sequential_statement','parser.py',192),
  ('parallel_statements -> parallel_statement par_sep parallel_statements','parallel_statements',3,'p_parallel_statements','parser.py',196),
  ('parallel_statements -> parallel_statement','parallel_statements',1,'p_parallel_statements_s','parser.py',200),
  ('parallel_statements -> parallel_statement par_sep','parallel_statements',2,'p_parallel_statements_s','parser.py',201),
  ('parallel_statement -> gate_statement','parallel_statement',1,'p_parallel_statement','parser.py',205),
  ('parallel_statement -> sequential_gate_block','parallel_statement',1,'p_parallel_statement','parser.py',206),
  ('array_declaration -> IDENTIFIER LBRACKET let_or_integer RBRACKET','array_declaration',4,'p_array_declaration','parser.py',210),
  ('array_element -> IDENTIFIER LBRACKET let_or_integer RBRACKET','array_element',4,'p_array_element','parser.py',214),
  ('array_slice -> IDENTIFIER LBRACKET slice_indexing RBRACKET','array_slice',4,'p_array_slice','parser.py',218),
  ('slice_indexing -> let_or_integer','slice_indexing',1,'p_slice_indexing_one','parser.py',222),
  ('slice_indexing -> let_or_integer COLON let_or_integer','slice_indexing',3,'p_slice_indexing_two','parser.py',226),
  ('slice_indexing -> let_or_integer COLON let_or_integer COLON let_or_integer','slice_indexing',5,'p_slice_indexing_three','parser.py',230),
  ('let_or_integer -> IDENTIFIER','let_or_integer',1,'p_let_or_integer','parser.py',234),
  ('let_or_integer -> INTEGER','let_or_integer',1,'p_let_or_integer','parser.py',235),
  ('seq_sep -> SEMICOLON','seq_sep',1,'p_seq_sep','parser.py',239),
  ('seq_sep -> EOL','seq_sep',1,'p_seq_sep','parser.py',240),
  ('seq_sep -> seq_sep EOL','seq_sep',2,'p_seq_sep','parser.py',241),
  ('par_sep -> PIPE','par_sep',1,'p_par_sep','parser.py',245),
  ('par_sep -> EOL','par_sep',1,'p_par_sep','parser.py',246),
  ('par_sep -> par_sep EOL','par_sep',2,'p_par_sep','parser.py',247),
  ('number -> INTEGER','number',1,'p_number','parser.py',251),
  ('number -> FLOAT','number',1,'p_number','parser.py',252),
]