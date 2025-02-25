import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # TTK widgets
import threading
import time
import re
import pandas as pd
import json
import os
import tkinter.font as tkfont
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET


# Embed the XML content as a multi-line string.
MDF_XML = r"""<!--=====================================================================
Mapping file to import MDF standard format files into FieldWorks or some other application.
See documentation in Lexicon Import.htm for information on customizing/using this file.
=====================================================================-->
<sfmMapping>

<!--=====================================================================
Global Settings
=====================================================================-->
<settings>
<meaning app="fw.sil.org"/>
</settings>

<!--=====================================================================
Language Definitions
=====================================================================-->
<languages>
<langDef id="English" xml:lang="en"/>
<langDef id="Vernacular" xml:lang ="Vernacular"/>
<langDef id="Regional" xml:lang ="ignore"/>
<langDef id="National" xml:lang ="ignore"/>
</languages>

<!--=====================================================================
Level Hierarchy
=====================================================================-->
<hierarchy>
<level name="Entry" partOf="records" beginFields="lx" additionalFields="a bw ce cf cn cr dt hm lc mn mr ph" multiFields="a bw ce cf cn cr lc mn mr ph"/>
<level name="Subentry" partOf="Entry" beginFields="se" additionalFields="bw ce cf cn cr mn mr ph" multiFields="bw ce cf cn cr mn mr ph"/>
<level name="Sense" partOf="Entry Subentry" beginFields="ge ps sn" additionalFields="1d 1e 1i 1p 1s 2d 2p 2s 3d 3p 3s 4d 4p 4s an bb de dn dr dv ee en er ev exm gn gr gv lt na nd ng np nq ns nt oe on or ov pc pd pde pdl pdn pdr pdv pl pn rd re rn rr sc sg so st sy tb ue un ur uv we wn wr" multiFields="1d 1e 1i 1p 1s 2d 2p 2s 3d 3p 3s 4d 4p 4s an bb de dn dr dv ee en er ev exm ge gn gr gv is lt na nd ng np nq ns nt oe on or ov pc pd pde pdl pdn pdr pdv pl pn rd re rn rr sc sd sg so st sy tb th ue un ur uv we wn wr"/>
<level name="Etymology" partOf="Entry Subentry" beginFields="et" additionalFields="ec eg es" multiFields="ec eg"/>
<level name="Example" partOf="Sense" beginFields="rf xv" additionalFields="" multiFields=""/>
<level name="ExampleTranslation" partOf="Example" beginFields="xe" additionalFields="xn xr" multiFields="xn xr"/>
<level name="ExtendedNote" partOf="Sense" beginFields="ent end" additionalFields="" multiFields="end"/>
<level name="ExtendedNoteExample" partOf="ExtendedNote" beginFields="enex" additionalFields="" multiFields=""/>
<level name="ExtendedNoteExampleTranslation" partOf="ExtendedNoteExample" beginFields="entr" additionalFields="" multiFields=""/>
<level name="Function" partOf="Sense" beginFields="lf" additionalFields="lv"/>
<level name="SemanticDomain" partOf="Sense" beginFields="is" additionalFields="sd th"/>
<level name="Picture" partOf="Sense" beginFields="pc" additionalFields=""/>
<level name="Pronunciation" partOf="Entry Subentry" beginFields="ph" additionalFields=""/>
<level name="Variant" partOf="Entry Subentry" beginFields="va" additionalFields="ve vn vr"/>
</hierarchy>

<!--=====================================================================
Field Descriptions
=====================================================================-->
<fieldDescriptions>
<field sfm="1d" name="First dual" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="1e" name="First plural exclusive" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="1i" name="First plural inclusive" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="1p" name="First plural" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="1s" name="First singular" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="2d" name="Second dual" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="2p" name="Second plural" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="2s" name="Second singular" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="3d" name="Third dual" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="3p" name="Third plural" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="3s" name="Third singular" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="4d" name="Non-animate dual" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="4p" name="Non-animate plural" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="4s" name="Non-animate singular" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="a" name="Allomorph" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="allo"/>
</field>
<field sfm="an" name="Antonym Lexical Relation" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="lxrel" funcWS="en" func="Antonym"/>
</field>
<field sfm="bb" name="Bibliography" type="string" lang="English">
<meaning app="fw.sil.org" id="sbib"/>
</field>
<field sfm="bw" name="Borrowed word (language)" type="string" lang="English">
<meaning app="fw.sil.org" id="etsl"/>
</field>
<field sfm="ce" name="Cross-ref. gloss (English)" type="string" lang="English">
<meaning app="fw.sil.org" id="eires"/>
</field>
<field sfm="cf" name="Compare Cross Reference" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="cref" funcWS="en" func="Compare"/>
</field>
<field sfm="cn" name="Cross-ref. gloss (national)" type="string" lang="National">
<meaning app="fw.sil.org" id="eires"/>
</field>
<field sfm="cr" name="Cross-ref. gloss (regional)" type="string" lang="National">
<meaning app="fw.sil.org" id="eires"/>
</field>
<field sfm="de" name="Definition" type="string" lang="English">
<meaning app="fw.sil.org" id="def"/>
</field>
<field sfm="dn" name="Definition" type="string" lang="National">
<meaning app="fw.sil.org" id="def"/>
</field>
<field sfm="dr" name="Definition" type="string" lang="Regional">
<meaning app="fw.sil.org" id="def"/>
</field>
<field sfm="dt" name="Date Modified" type="date" lang="English">
<meaning app="fw.sil.org" id="mod"/>
</field>
<field sfm="dv" name="Definition" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="def"/>
</field>
<field sfm="ec" name="Etymology Comment" type="string" lang="English">
<meaning app="fw.sil.org" id="etc"/>
</field>
<field sfm="ee" name="Encyclopedic Information" type="string" lang="English">
<meaning app="fw.sil.org" id="enc"/>
</field>
<field sfm="eg" name="Etymology Gloss" type="string" lang="English">
<meaning app="fw.sil.org" id="etg"/>
</field>
<field sfm="en" name="Encyclopedic Information" type="string" lang="National">
<meaning app="fw.sil.org" id="enc"/>
</field>
<field sfm="end" name="Extended Note Discussion" type="string" lang="English">
<meaning app="fw.sil.org" id="end"/>
</field>
<field sfm="ent" name="Extended Note Type" type="string" lang="English">
<meaning app="fw.sil.org" id="ent"/>
</field>
<field sfm="enex" name="Extended Note Example" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="enex"/>
</field>
<field sfm="entr" name="Extended Note Example Translation" type="string" lang="English">
<meaning app="fw.sil.org" id="entr"/>
</field>
<field sfm="er" name="Encyclopedic Information" type="string" lang="Regional">
<meaning app="fw.sil.org" id="enc"/>
</field>
<field sfm="es" name="Etymology Source" type="string" lang="English">
<meaning app="fw.sil.org" id="ets"/>
</field>
<field sfm="et" name="Etymology (proto form)" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="etf"/>
</field>
<field sfm="ev" name="Encyclopedic Information" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="enc"/>
</field>
<field sfm="exm" name="Exemplar" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="exm"/>
</field>
<field sfm="ge" name="Gloss" type="string" lang="English">
<meaning app="fw.sil.org" id="glos"/>
</field>
<field sfm="gn" name="Gloss" type="string" lang="National">
<meaning app="fw.sil.org" id="glos"/>
</field>
<field sfm="gr" name="Gloss" type="string" lang="Regional">
<meaning app="fw.sil.org" id="glos"/>
</field>
<field sfm="gv" name="Gloss" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="glos"/>
</field>
<field sfm="hm" name="Homonym number" type="integer" lang="English">
<meaning app="fw.sil.org" id="hom"/>
</field>
<field sfm="is" name="Semantic Domain" type="string" lang="English" abbr="true">
<meaning app="fw.sil.org" id="sem"/>
</field>
<field sfm="lc" name="Citation Form" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="cit"/>
</field>
<field sfm="le" name="Lexical function gloss (English)" type="string" lang="English">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="lf" name="Lexical Function" type="string" lang="English" abbr="true">
<meaning app="fw.sil.org" id="func"/>
</field>
<!--field sfm="lf" name="Lexical Function and Lexeme" type="string" lang="Vernacular" abbr="true">
<meaning app="fw.sil.org" id="funold" funcWS="en"/>
</field-->
<field sfm="ln" name="Lexical function gloss (national)" type="string" lang="National">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="lr" name="Lexical function gloss (regional)" type="string" lang="Regional">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="lt" name="Literally" type="string" lang="English">
<meaning app="fw.sil.org" id="litm"/>
</field>
<field sfm="lv" name="Lexical Function Lexeme" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="funlex"/>
</field>
<field sfm="lx" name="Lexeme" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="lex"/>
</field>
<field sfm="mn" name="Main Entry Reference" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="meref"/>
</field>
<field sfm="mr" name="Morphology" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="eires"/>
</field>
<field sfm="na" name="Anthro  Note" type="string" lang="English">
<meaning app="fw.sil.org" id="anote"/>
</field>
<field sfm="nd" name="Discourse Note" type="string" lang="English">
<meaning app="fw.sil.org" id="dnote"/>
</field>
<field sfm="ng" name="GrammarNote" type="string" lang="English">
<meaning app="fw.sil.org" id="grnote"/>
</field>
<field sfm="np" name="Phonology Note" type="string" lang="English">
<meaning app="fw.sil.org" id="pnote"/>
</field>
<field sfm="nq" name="Notes (questions)" type="string" lang="English">
<meaning app="fw.sil.org" id="gnote"/>
</field>
<field sfm="ns" name="Sociolinguistics Note" type="string" lang="English">
<meaning app="fw.sil.org" id="slnote"/>
</field>
<field sfm="nt" name="General Note" type="string" lang="English">
<meaning app="fw.sil.org" id="gnote"/>
</field>
<field sfm="oe" name="Restrictions" type="string" lang="English">
<meaning app="fw.sil.org" id="srest"/>
</field>
<field sfm="on" name="Restrictions" type="string" lang="National">
<meaning app="fw.sil.org" id="srest"/>
</field>
<field sfm="or" name="Restrictions" type="string" lang="Regional">
<meaning app="fw.sil.org" id="srest"/>
</field>
<field sfm="ov" name="Restrictions" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="srest"/>
</field>
<field sfm="pc" name="Picture" type="string" lang="English">
<meaning app="fw.sil.org" id="picf"/>
</field>
<field sfm="pd" name="Paradigm" type="string" lang="English">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="pde" name="Paradigm form gloss (English)" type="string" lang="English">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="pdl" name="Paradigm label" type="string" lang="English">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="pdn" name="Paradigm form gloss (national)" type="string" lang="National">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="pdr" name="Paradigm form gloss (regional)" type="string" lang="Regional">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="pdv" name="Paradigm form" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="ph" name="Phonetic form" type="string" lang="phonetic">
<meaning app="fw.sil.org" id="prnf"/>
</field>
<field sfm="pl" name="Plural form" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="pn" name="Part of speech (national)" type="string" lang="National">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="ps" name="Part of Speech" type="string" lang="English" abbr="true">
<meaning app="fw.sil.org" id="pos"/>
</field>
<field sfm="rd" name="Reduplication form(s)" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="re" name="Reversal" type="string" lang="English">
<meaning app="fw.sil.org" id="rev"/>
</field>
<field sfm="rf" name="Reference of Example Sentence" type="string" lang="English">
<meaning app="fw.sil.org" id="ref"/>
</field>
<field sfm="rn" name="Reversal" type="string" lang="National">
<meaning app="fw.sil.org" id="rev"/>
</field>
<field sfm="rr" name="Reversal" type="string" lang="Regional">
<meaning app="fw.sil.org" id="rev"/>
</field>
<field sfm="sc" name="Scientific Name" type="string" lang="English">
<meaning app="fw.sil.org" id="sci"/>
</field>
<field sfm="sd" name="Semantic Domain English Name" type="string" lang="English">
<meaning app="fw.sil.org" id="seme"/>
</field>
<field sfm="se" name="Subentry" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sub" funcWS="en" func="Unspecified Complex Form"/>
</field>
<field sfm="sg" name="Singular form" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="sn" name="Sense Number" type="string" lang="English">
<meaning app="fw.sil.org" id="sn"/>
</field>
<field sfm="so" name="Source" type="string" lang="English">
<meaning app="fw.sil.org" id="src"/>
</field>
<field sfm="st" name="Status" type="string" lang="English">
<meaning app="fw.sil.org" id="stat"/>
</field>
<field sfm="sy" name="Synonym Lexical Relation" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="lxrel" funcWS="en" func="Synonyms"/>
</field>
<field sfm="tb" name="Table" type="string" lang="English">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="th" name="Semantic Domain Vernacular Name" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="semv"/>
</field>
<field sfm="ue" name="Usage" type="string" lang="English">
<meaning app="fw.sil.org" id="utyp"/>
</field>
<field sfm="un" name="Usage (national)" type="string" lang="National">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="ur" name="Usage (regional)" type="string" lang="Regional">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="uv" name="Usage (vernacular)" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="va" name="Variant" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="var" funcWS="en" func="Unspecified Variant" />
</field>
<field sfm="ve" name="Variant Comment" type="string" lang="English">
<meaning app="fw.sil.org" id="varc"/>
</field>
<field sfm="vn" name="Variant Comment" type="string" lang="National">
<meaning app="fw.sil.org" id="varc"/>
</field>
<field sfm="vr" name="Variant Comment" type="string" lang="Regional">
<meaning app="fw.sil.org" id="varc"/>
</field>
<field sfm="we" name="Word-level gloss (English)" type="string" lang="English">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="wn" name="Word-level gloss (national)" type="string" lang="National">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="wr" name="Word-level gloss (regional)" type="string" lang="Regional">
<meaning app="fw.sil.org" id="sires"/>
</field>
<field sfm="xe" name=" Translation of Example Sentence" type="string" lang="English">
<meaning app="fw.sil.org" id="trans"/>
</field>
<field sfm="xn" name="Translation of Example Sentence" type="string" lang="National">
<meaning app="fw.sil.org" id="trans"/>
</field>
<field sfm="xr" name="Translation of Example Sentence" type="string" lang="Regional">
<meaning app="fw.sil.org" id="trans"/>
</field>
<field sfm="xv" name="Example Sentence in Vernacular" type="string" lang="Vernacular">
<meaning app="fw.sil.org" id="sent"/>
</field>
</fieldDescriptions>

<!--=====================================================================
In Field Markers (inline markers)
=====================================================================-->
<inFieldMarkers>
	<!-- <ifm element="Remove" begin="|xx" end="*|xx" ignore="true" lang="Vernacular" style="Emphasized Text"/> -->
</inFieldMarkers>

</sfmMapping>
"""

# --------------------------------------------------------------------------
# 2. Helper function: Load the MDF hierarchy from the XML string.
# --------------------------------------------------------------------------
def load_hierarchy_from_string(xml_string):
    """
    Parse the MDF XML string and return a list of levels,
    each represented as a dictionary with keys:
      - name
      - beginFields (a list)
      - additionalFields (a list)
      - multiFields (a list)
      - partOf (a list)
    """
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root_xml = tree.getroot()
    hierarchy = []
    hierarchy_xml = root_xml.find('hierarchy')
    if hierarchy_xml is not None:
        for level in hierarchy_xml.findall('level'):
            level_info = {
                'name': level.get('name'),
                'beginFields': level.get('beginFields', '').split(),
                'additionalFields': level.get('additionalFields', '').split(),
                'multiFields': level.get('multiFields', '').split(),
                'partOf': level.get('partOf', '').split()
            }
            hierarchy.append(level_info)
    return hierarchy

# Load the MDF hierarchy from the embedded XML.
mdf_hierarchy = load_hierarchy_from_string(MDF_XML)

# --------------------------------------------------------------------------
# 3. Build a marker-to-level map from the MDF hierarchy.
# --------------------------------------------------------------------------
def build_marker_level_map(hierarchy):
    """
    Given the hierarchy from the MDF XML mapping file,
    returns a dictionary mapping each marker (with a leading "\")
    to its level (e.g., "Entry", "Sense", etc.).
    """
    marker_map = {}
    for level in hierarchy:
        level_name = level.get('name', 'Entry')
        for field in level.get('beginFields', []):
            if field:
                marker_map["\\" + field] = level_name
        for field in level.get('additionalFields', []):
            if field:
                marker_map["\\" + field] = level_name
        for field in level.get('multiFields', []):
            if field:
                marker_map["\\" + field] = level_name
    return marker_map

# Build the marker-level map.
marker_level_map = build_marker_level_map(mdf_hierarchy)

# --------------------------------------------------------------------------
# 4. Build level field sets from the hierarchy (for determining begin markers).
# --------------------------------------------------------------------------
def build_level_field_sets(hierarchy):
    """
    Create a dictionary mapping each level to its sets of fields.
    """
    level_field = {}
    for level in hierarchy:
        name = level['name']
        level_field[name] = {
            "begin": set(level.get('beginFields', [])),
            "additional": set(level.get('additionalFields', [])),
            "multi": set(level.get('multiFields', []))
        }
    return level_field

level_fields = build_level_field_sets(mdf_hierarchy)

# --------------------------------------------------------------------------
# 2. Helper function: Load the MDF hierarchy from the XML string.
# --------------------------------------------------------------------------
def load_hierarchy_from_string(xml_string):
    """
    Parse the MDF XML string and return a list of levels,
    each represented as a dictionary with keys:
      - name
      - beginFields (a list)
      - additionalFields (a list)
      - multiFields (a list)
      - partOf (a list)
    """
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root_xml = tree.getroot()
    hierarchy = []
    hierarchy_xml = root_xml.find('hierarchy')
    if hierarchy_xml is not None:
        for level in hierarchy_xml.findall('level'):
            level_info = {
                'name': level.get('name'),
                'beginFields': level.get('beginFields', '').split(),
                'additionalFields': level.get('additionalFields', '').split(),
                'multiFields': level.get('multiFields', '').split(),
                'partOf': level.get('partOf', '').split()
            }
            hierarchy.append(level_info)
    return hierarchy

# Load the MDF hierarchy from the embedded XML.
mdf_hierarchy = load_hierarchy_from_string(MDF_XML)

# --------------------------------------------------------------------------
# 3. Build a marker-to-level map from the MDF hierarchy.
# --------------------------------------------------------------------------
def build_marker_level_map(hierarchy):
    """
    Given the hierarchy from the MDF XML mapping file,
    returns a dictionary mapping each marker (with a leading "\")
    to its level (e.g., "Entry", "Sense", etc.).
    """
    marker_map = {}
    for level in hierarchy:
        level_name = level.get('name', 'Entry')
        for field in level.get('beginFields', []):
            if field:
                marker_map["\\" + field] = level_name
        for field in level.get('additionalFields', []):
            if field:
                marker_map["\\" + field] = level_name
        for field in level.get('multiFields', []):
            if field:
                marker_map["\\" + field] = level_name
    return marker_map

# Build the marker-level map.
marker_level_map = build_marker_level_map(mdf_hierarchy)

# --------------------------------------------------------------------------
# 4. Build level field sets from the hierarchy (for determining begin markers).
# --------------------------------------------------------------------------
def build_level_field_sets(hierarchy):
    """
    Create a dictionary mapping each level to its sets of fields.
    """
    level_field = {}
    for level in hierarchy:
        name = level['name']
        level_field[name] = {
            "begin": set(level.get('beginFields', [])),
            "additional": set(level.get('additionalFields', [])),
            "multi": set(level.get('multiFields', []))
        }
    return level_field

level_fields = build_level_field_sets(mdf_hierarchy)

def flatten_entries_with_hierarchy(entries):
    """
    Convert a list of nested entry dictionaries into a flat table,
    but DO NOT include level prefixes like 'Entry:' or 'Sense:'.
    
    For each entry (lexicon record):
      - The "Entry" level is a dictionary with markers -> list of values.
      - Other levels (like "Sense") are stored as a list of dictionaries.
    
    Column headers will be just the marker name for entry-level,
    and for sense-level we append _1, _2, etc. to handle multiple senses.
    """
    flattened = []

    for entry in entries:
        flat_entry = {}
        
        # Process the "Entry" level
        for marker, values in entry.get("Entry", {}).items():
            # e.g. marker == "\lx"
            # Join multiple values with "|"
            flat_entry[marker] = " | ".join(values)

        # Process each other level (e.g. "Sense", "Subentry", etc.)
        for level_name in entry:
            if level_name == "Entry":
                continue  # already handled
            # If this level is a list of dictionaries
            for idx, instance in enumerate(entry[level_name], start=1):
                for marker, values in instance.items():
                    # build a column name like "\lx_1", "\lx_2", etc.
                    col_name = f"{marker}_{idx}"
                    flat_entry[col_name] = " | ".join(values)

        flattened.append(flat_entry)

    # Convert list of dicts to a DataFrame
    df = pd.DataFrame(flattened)
    return df




###############################################################################
# 1) Define sets for certain known markers.
#    - ENTRY_MARKERS: always treated as entry-level.
#    - SENSE_MARKERS: always treated as sense-level (e.g., \sn).
###############################################################################

ENTRY_MARKERS = {
    "\\a",    # Allomorph
    "\\bw",   # Borrowed word (language)
    "\\ce",   # Cross-ref. gloss (English)
    "\\cf",   # Cross reference
    "\\cn",   # Cross-ref. gloss (national)
    "\\cr",   # Cross-ref. gloss (regional)
    "\\dt",   # Date
    "\\ec",   # Etymology comment
    "\\eg",   # Etymology gloss
    "\\es",   # Etymology source language notes
    "\\esl",  # Etymology source language
    "\\et",   # Etymology source language form
    "\\hm",   # Homograph number    
    "\\lc",   # Citation form
    "\\lf",   # Lexeme form
    "\\lt",   # Literally
    "\\lv",   # Lexical function lexeme
    "\\lx",   # Lexeme
    "\\mn",   # Main entry cross-reference
    "\\mr",   # Morphology (additional info)
    "\\ph",   # Phonemic form
    "\\se",   # Subentry
    "\\va",   # Variant forms
    "\\ve",   # Variant comment English
    "\\vn",   # Variant comment National language
    "\\vr"    # Variant comment Regional language
}

SENSE_MARKERS = {
    "\\an",   # Antonym
    "\\bb",   # Bibliography
    "\\de",   # Definition (English)
    "\\dn",   # Definition (National)
    "\\dr",   # Definition (Regional)
    "\\dv",   # Definition (Vernacular)
    "\\ee",   # Encyclopedic info (English)
    "\\en",   # Encyclopedic info (National)
    "\\er",   # Encyclopedic info (Regional)
    "\\ev",   # Encyclopedic info (Vernacular)
    "\\ge",   # Gloss (English)
    "\\gn",   # Gloss (National)
    "\\gr",   # Gloss (Regional)
    "\\gv",   # Gloss (Vernacular)
    "\\na",   # Anthropology note
    "\\nd",   # Discourse note
    "\\ng",   # Grammar note
    "\\np",   # Note pronunciation
    "\\nq",   # Questions/notes
    "\\ns",   # Sociolinguistics note
    "\\nt",   # General note
    "\\oe",   # Restrictions (English)
    "\\on",   # Restrictions (National)
    "\\or",   # Restrictions (Regional)
    "\\ov",   # Restrictions (Vernacular)
    "\\ps",   # Part of speech
    "\\re",   # Reversal (English)
    "\\rf",   # Reference for example sentence
    "\\rn",   # Reversal (National)
    "\\rr",   # Reversal (Regional)
    "\\sc",   # Scientific name
    "\\sn",   # Sense number
    "\\so",   # Source
    "\\st",   # Status
    "\\sy",   # Synonym
    "\\ue",   # Usage
    "\\xe",   # Example translation (English)
    "\\xn",   # Example translation (National)
    "\\xr",   # Example translation (Regional)
    "\\xv",   # Example sentence (Vernacular)
    "\\exm",  # Exemplar
    "\\pc",   # Picture
    "\\pd",   # Paradigm
    "\\pde",  # Paradigm form gloss (English)
    "\\pdl",  # Paradigm label
    "\\pdn",  # Paradigm form gloss (National)
    "\\pdr",  # Paradigm form gloss (Regional)
    "\\pdv",  # Paradigm form (Vernacular)
    "\\pl",   # Plural form
    "\\pn",   # Part of speech (national) [if used separately]
    "\\rd",   # Reduplication form(s)
    "\\sg",   # Singular form
    "\\tb",   # Table
    "\\un",   # Usage (National)
    "\\ur",   # Usage (Regional)
    "\\uv",   # Usage (Vernacular)
    "\\we",   # Word-level gloss (English)
    "\\wn",   # Word-level gloss (National)
    "\\wr"    # Word-level gloss (Regional)
}

###############################################################################
# 2) Define prefixes that, if found in the marker, make it sense-level or
#    entry-level.
###############################################################################

ENTRY_PREFIXES = [
    "a",    # e.g. \a_Eng
    "bw",   # e.g. \bw_Eng
    "ce",   # e.g. \ce_Eng
    "cn",   # e.g. \cn_Eng
    "cr",   # e.g. \cr_Eng
    "ea",   # e.g. \ea_Eng, \ea_Lad (etymology preceding annotations)
    "eb",   # e.g. \eb_Eng, \eb_Lad (etymology bibliography)
    "efc",  # e.g. \efc_Eng, \efc_Lad (etymology following comments)
    "eg",   # e.g. \eg_Eng, \eg_Lad (etymology gloss)
    "es",   # e.g. \es_Eng, \es_Lad (etymology source language notes)
    "et",   # e.g. \et_Eng, \et_Lad (etymology source language form)
    "v"     # e.g. \v_Eng, \v_Lad (variant comments)
]

SENSE_PREFIXES = [
    "an",   # e.g. \an_Eng, \an_Lad (antonym)
    "bb",   # e.g. \bb_Eng, \bb_Lad (bibliography)
    "d",    # e.g. \d_Eng, \d_Tib (definition)
    "e",    # e.g. \e_Eng, \e_Lad (encyclopedic info)
    "g",    # e.g. \g_Eng, \g_Hin (gloss)
    "na",   # e.g. \na_Eng, \na_Lad (anthropology note)
    "nd",   # e.g. \nd_Eng, \nd_Lad (discourse note)
    "ng",   # e.g. \ng_Eng, \ng_Lad (grammar note)
    "nq",   # e.g. \nq_Eng, \nq_Lad (questions/notes)
    "ns",   # e.g. \ns_Eng, \ns_Lad (sociolinguistics note)
    "nt",   # e.g. \nt_Eng, \nt_Lad (general note)
    "o",    # e.g. \o_Eng, \o_Lad (restrictions)
    "ps",   # e.g. \ps_Eng, \ps_Lad (part of speech)
    "r",    # e.g. \r_Eng, \r_Lad (reversal)
    "sc",   # e.g. \sc_Eng, \sc_Lad (scientific name)
    "so",   # e.g. \so_Eng, \so_Lad (source)
    "st",   # e.g. \st_Eng, \st_Lad (status)
    "sy",   # e.g. \sy_Eng, \sy_Lad (synonym)
    "u",    # e.g. \u_Eng, \u_Lad (usage)
    "x",    # e.g. \x_Eng, \x_Lad (examples)
    "xv",   # e.g. \xv_Lad-Latn, \xv_Lad-Ucen (example sentence in Vernacular)
    "exm",  # e.g. \exm_Eng (exemplar)
    "pd",   # paradigm
    "pde",  # paradigm form gloss (English)
    "pdl",  # paradigm label
    "pdn",  # paradigm form gloss (National)
    "pdr",  # paradigm form gloss (Regional)
    "pdv",  # paradigm form (Vernacular)
    "pl",   # plural form
    "pn",   # part of speech (national) [if used separately]
    "rd",   # reduplication form(s)
    "sg",   # singular form
    "tb",   # table
    "un",   # usage (National)
    "ur",   # usage (Regional)
    "uv",   # usage (Vernacular)
    "we",   # word-level gloss (English)
    "wn",   # word-level gloss (National)
    "wr"    # word-level gloss (Regional)
]

###############################################################################
# 3) A helper function to decide if a marker is sense-level or entry-level.
###############################################################################

def is_sense_marker(marker: str) -> bool:
    """
    Returns True if marker is sense-level, False if entry-level.
    """
    if marker in SENSE_MARKERS:
        return True
    if marker in ENTRY_MARKERS:
        return False
    sense_pattern = r'^\\(' + '|'.join(SENSE_PREFIXES) + r')_.+'
    if re.match(sense_pattern, marker):
        return True
    entry_pattern = r'^\\(' + '|'.join(ENTRY_PREFIXES) + r')_.+'
    if re.match(entry_pattern, marker):
        return False
    return False

###############################################################################
# Conversion functions: parse_sfm, compute_max_occurrences, flatten_entries.
###############################################################################

def parse_sfm(file_path):
    """
    Parse an SFM file. Repeated occurrences of a marker are stored as a list.
    - Sense-level markers (as determined by is_sense_marker) go to the current sense.
    - Entry-level markers go to the entry-level dictionary.
    - \\sn always starts a new sense dictionary.
    """
    entries = []
    current_entry = None
    current_sense = None
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_entry is not None:
                    entries.append(current_entry)
                current_entry = None
                current_sense = None
                continue

            if not line.startswith('\\'):
                continue

            parts = line.split(' ', 1)
            marker = parts[0]
            value = parts[1] if len(parts) > 1 else ""

            if current_entry is None:
                current_entry = {"lex": {}, "senses": []}
                current_sense = None

            if marker == "\\lx":
                # If we already had an entry in progress, close it out
                if current_entry and (current_entry["lex"] or current_entry["senses"]):
                    entries.append(current_entry)
                current_entry = {"lex": {}, "senses": []}
                current_sense = None
                current_entry["lex"].setdefault(marker, []).append(value)
            elif marker == "\\sn":
                current_sense = {marker: [value]}
                current_entry["senses"].append(current_sense)
            else:
                if is_sense_marker(marker):
                    if not current_entry["senses"]:
                        current_sense = {"\\sn": ["1"]}
                        current_entry["senses"].append(current_sense)
                    elif current_sense is None:
                        current_sense = {}
                        current_entry["senses"].append(current_sense)
                    current_sense.setdefault(marker, []).append(value)
                else:
                    current_entry["lex"].setdefault(marker, []).append(value)

    if current_entry and (current_entry["lex"] or current_entry["senses"]):
        entries.append(current_entry)
    return entries

def compute_max_occurrences(entries):
    """
    Determine the maximum number of occurrences for each marker at the entry level and sense level,
    plus the max number of senses across all entries.
    """
    lex_marker_occurrences = {}
    sense_marker_occurrences = {}
    max_senses = 0

    for entry in entries:
        for marker, values in entry["lex"].items():
            count = len(values)
            if count > lex_marker_occurrences.get(marker, 0):
                lex_marker_occurrences[marker] = count

        num_senses = len(entry["senses"])
        if num_senses > max_senses:
            max_senses = num_senses

        for sense in entry["senses"]:
            for marker, values in sense.items():
                count = len(values)
                if count > sense_marker_occurrences.get(marker, 0):
                    sense_marker_occurrences[marker] = count

    return lex_marker_occurrences, sense_marker_occurrences, max_senses

def flatten_entries(entries):
    """
    Flatten entries into one row per lexeme.
    Repeated markers generate repeated columns.
    For sense-level markers, repeat for each sense; the \\sn column is ensured to come first.
    """
    lex_marker_occurrences, sense_marker_occurrences, max_senses = compute_max_occurrences(entries)

    lex_markers = sorted(lex_marker_occurrences.keys())

    def sense_sort_key(m):
        return (m != '\\sn', m)
    sense_markers = sorted(sense_marker_occurrences.keys(), key=sense_sort_key)

    columns = []
    # Add columns for each lexeme-level marker
    for marker in lex_markers:
        columns += [marker] * lex_marker_occurrences[marker]

    # Add columns for sense-level markers
    for sense_index in range(1, max_senses + 1):
        for marker in sense_markers:
            columns += [f"{marker}_{sense_index}"] * sense_marker_occurrences[marker]

    rows = []
    for entry in entries:
        row_values = []
        # Fill lexeme-level columns
        for marker in lex_markers:
            needed = lex_marker_occurrences[marker]
            actual = entry["lex"].get(marker, [])
            actual += [""] * (needed - len(actual))
            row_values.extend(actual)

        # Fill sense-level columns
        for sense_index in range(max_senses):
            sense_data = entry["senses"][sense_index] if sense_index < len(entry["senses"]) else {}
            for marker in sense_markers:
                needed = sense_marker_occurrences[marker]
                actual = sense_data.get(marker, [])
                actual += [""] * (needed - len(actual))
                row_values.extend(actual)

        rows.append(row_values)

    df = pd.DataFrame(rows, columns=columns)

    # Remove numeric suffixes like _1, _2, etc.
    def remove_suffix(col):
        if "_" in col:
            base, suffix = col.rsplit("_", 1)
            if suffix.isdigit():
                return base
        return col
    df.rename(columns=remove_suffix, inplace=True)

    # FIX 1: Rename any column name that is empty (or all whitespace) to "UNKNOWN_MARKER"
    df.rename(
        columns=lambda c: c.strip() if c.strip() else "UNKNOWN_MARKER",
        inplace=True
    )

    return df

###############################################################################
# Preferences, Logging, and Global Variables
###############################################################################

CONFIG_PATH = "settings.json"

def load_settings():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {"default_font": "Arial", "last_folder": ""}

def save_settings(settings):
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def show_preferences():
    prefs_win = tk.Toplevel(root)
    prefs_win.title("Preferences")
    prefs_win.geometry("300x200")
    settings = load_settings()

    ttk.Label(prefs_win, text="Default Font:").pack(pady=5)
    all_fonts = sorted(tkfont.families())
    font_var = tk.StringVar(value=settings.get("default_font", "Arial"))
    font_combo = ttk.Combobox(prefs_win, textvariable=font_var, values=all_fonts)
    font_combo.pack(pady=5)

    def apply_prefs():
        settings["default_font"] = font_var.get()
        save_settings(settings)
        prefs_win.destroy()

    ttk.Button(prefs_win, text="Save", command=apply_prefs).pack(pady=10)

def log_message(msg):
    log_text.config(state='normal')
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')

# Global variables for DataFrame and suggested filename
converted_df = None
converted_filename = "output.xlsx"

###############################################################################
# Preview
###############################################################################

def show_preview(df):
    """
    Use unique column IDs for Treeview to avoid blank headings for duplicates.
    """
    for item in preview_tree.get_children():
        preview_tree.delete(item)

    cols = list(df.columns)
    unique_ids = [f"col_{i}" for i in range(len(cols))]
    preview_tree.config(columns=unique_ids, show='headings')

    for i, col_name in enumerate(cols):
        col_id = unique_ids[i]
        preview_tree.heading(col_id, text=col_name)
        preview_tree.column(col_id, width=120, anchor='center')

    preview_data = df.head(10).values.tolist()
    for row_data in preview_data:
        preview_tree.insert("", "end", values=row_data)

def parse_sfm_with_hierarchy(file_path):
    """
    A minimal hierarchical parser that organizes data into a nested structure:
      {
        "Entry": { marker -> [values], ... },
        "Sense": [ { marker -> [values], ... }, ... ]
      }

    In this simple version:
      - A line starting with \lx begins a new "Entry" block.
      - A line starting with \sn (or any sense-begin marker) begins a new "Sense" block.
      - All sense-level markers go into the current sense dictionary.
      - All entry-level markers go into the "Entry" dictionary.
    
    This does NOT handle Subentries, Examples, or other levels yet.
    Expand as needed for your MDF hierarchy.
    """
    entries = []
    current_entry = None
    current_sense = None

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                # Blank line => end of current entry
                if current_entry is not None:
                    entries.append(current_entry)
                current_entry = None
                current_sense = None
                continue

            # Skip lines that don't start with a backslash
            if not line.startswith('\\'):
                continue

            # Split into marker + value
            parts = line.split(' ', 1)
            marker = parts[0]
            value = parts[1] if len(parts) > 1 else ""

            # If no entry started yet, create one
            if current_entry is None:
                current_entry = {
                    "Entry": {},  # Dictionary for entry-level markers
                    "Sense": []   # List of sense dictionaries
                }
                current_sense = None

            # If we see \lx, that starts a new Entry
            if marker == "\\lx":
                # If there was a previous entry in progress, finalize it
                if current_entry and (current_entry["Entry"] or current_entry["Sense"]):
                    entries.append(current_entry)
                current_entry = {"Entry": {}, "Sense": []}
                current_sense = None
                current_entry["Entry"].setdefault(marker, []).append(value)

            # If we see \sn, that starts a new sense
            elif marker == "\\sn":
                current_sense = {marker: [value]}
                current_entry["Sense"].append(current_sense)

            else:
                # Decide if marker is sense-level or entry-level
                if is_sense_marker(marker):
                    # If no sense yet, create one
                    if not current_entry["Sense"]:
                        current_sense = {"\\sn": ["1"]}  # default sense number
                        current_entry["Sense"].append(current_sense)
                    elif current_sense is None:
                        current_sense = {}
                        current_entry["Sense"].append(current_sense)

                    current_sense.setdefault(marker, []).append(value)

                else:
                    # entry-level
                    current_entry["Entry"].setdefault(marker, []).append(value)

    # End of file: if there's an unclosed entry, add it
    if current_entry and (current_entry["Entry"] or current_entry["Sense"]):
        entries.append(current_entry)

    return entries

###############################################################################
# File Processing
###############################################################################

def process_file(file_path):
    global converted_df, converted_filename
    try:
        status_var.set(f"Parsing {os.path.basename(file_path)} ...")
        progress_bar.start()
        log_message(f"Started processing file: {file_path}")

        time.sleep(1)  # Simulate delay (or remove if not needed)

        # Use the new hierarchical parser:
        entries = parse_sfm_with_hierarchy(file_path)
        # Convert the nested entries into a flat DataFrame
        df = flatten_entries_with_hierarchy(entries)
        # (Optional) If you need to adjust headers further, do it here.
        converted_df = df

        # Suggest a filename based on the input file name.
        base = os.path.splitext(os.path.basename(file_path))[0]
        converted_filename = f"{base}.xlsx"

        def update_ui():
            notebook.select(review_frame)  # Switch to the Review tab
            show_preview(df)

        root.after(0, update_ui)
        status_var.set("File processed successfully!")
        log_message("File processed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")
        log_message(f"Error processing file: {e}")
    finally:
        progress_bar.stop()

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("SFM Files", "*.txt;*.sfm;*.db"), ("All Files", "*.*")]
    )
    if not file_path:
        return
    threading.Thread(target=process_file, args=(file_path,), daemon=True).start()

def on_review_save():
    if converted_df is None:
        messagebox.showwarning("No Data", "No spreadsheet data available to save.")
        return
    save_file(converted_df, initialfile=converted_filename)

def save_file(df, initialfile="output.xlsx"):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel File", "*.xlsx"), ("CSV File", "*.csv")],
        initialfile=initialfile
    )
    if save_path:
        try:
            if save_path.endswith(".csv"):
                df.to_csv(save_path, index=False)
            else:
                df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"File saved successfully!\n{save_path}")
            status_var.set("File saved successfully!")
            log_message(f"File saved: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
            log_message(f"Error saving file: {e}")

###############################################################################
# About
###############################################################################

def about_link_clicked(*args):
    messagebox.showinfo(
        "About SFM2Sheet Converter",
        "SFM2Sheet Converter\n"
        "Version 1.0\n"
        "Developed by Maaz Ahmad Shaikh\n"
        "Licensed under MIT\n\n"
        "GitHub: https://github.com/SFM2SheetConverter\n"
    )

def about():
    about_win = tk.Toplevel(root)
    about_win.title("About SFM2Sheet Converter")
    about_win.geometry("400x300")
    ttk.Label(about_win, text="SFM2Sheet Converter", font=("Helvetica", 16, "bold")).pack(pady=10)
    ttk.Label(about_win, text="Version 1.0").pack()
    ttk.Label(about_win, text="Developed by [Your Name]").pack()
    ttk.Label(about_win, text="Licensed under MIT").pack(pady=10)
    ttk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=10)

###############################################################################
# Build the TTK-based GUI
###############################################################################

root = tk.Tk()
root.title("SFM2Sheet Converter")
root.geometry("700x500")

style = ttk.Style()
style.theme_use('clam')

# Notebook with two tabs: Convert and Review.
notebook = ttk.Notebook(root)
convert_frame = ttk.Frame(notebook, padding="10")
review_frame = ttk.Frame(notebook, padding="10")
notebook.add(convert_frame, text="Convert")
notebook.add(review_frame, text="Review")
notebook.pack(expand=True, fill='both')

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 1) Setting the window icon and single image label
try:
    icon_path = resource_path("images/SFM2Sheet-Converter_logo.png")
    img_original = Image.open(icon_path)
    # Use LANCZOS for quality
    img_resized = img_original.resize((300, 200), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(img_resized)
    # Set window icon
    root.iconphoto(False, logo_img)
except Exception as e:
    print("Could not load/resize icon:", e)
    logo_img = None

# Convert Tab UI

# (A) The "Open File" button at the top
ttk.Label(convert_frame, text="Select an SFM file to convert:").pack(pady=10)
open_button = ttk.Button(convert_frame, text="Open File", command=open_file)
open_button.pack(pady=10)

# Show the scaled-down image
if logo_img:
    logo_label = ttk.Label(convert_frame, image=logo_img)
    logo_label.pack(pady=10)

# **Put About link here** so it appears above the text
about_link = ttk.Label(
    convert_frame,
    text="About SFM2Sheet Converter",
    foreground="blue",
    cursor="hand2"
)
about_link.pack(pady=10)
about_link.bind("<Button-1>", about_link_clicked)

# Then the text widget
log_text = tk.Text(convert_frame, height=8, state='disabled', wrap='word')
log_text.pack(expand=False, fill='x', pady=10)

# Review Tab UI
tree_frame = ttk.Frame(review_frame)
tree_frame.pack(expand=True, fill='both')

scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
scrollbar_x.pack(side='bottom', fill='x')
scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
scrollbar_y.pack(side='right', fill='y')

preview_tree = ttk.Treeview(
    tree_frame,
    show='headings',
    xscrollcommand=scrollbar_x.set,
    yscrollcommand=scrollbar_y.set
)
preview_tree.pack(expand=True, fill='both')
scrollbar_x.config(command=preview_tree.xview)
scrollbar_y.config(command=preview_tree.yview)

ttk.Label(review_frame, text="Preview (first 10 rows):").pack()

# "Save the spreadsheet" button
save_button = ttk.Button(review_frame, text="Save the spreadsheet", command=on_review_save)
save_button.pack(pady=10)

# Font chooser
font_label = ttk.Label(review_frame, text="Choose display font:")
font_label.pack(pady=5)

all_fonts = sorted(tkfont.families())
font_var = tk.StringVar(value="Arial")
font_combo = ttk.Combobox(review_frame, textvariable=font_var, values=all_fonts, state="readonly")
font_combo.pack(pady=5)

def on_font_change(*args):
    new_font = font_var.get()
    preview_tree.configure(style="Preview.Treeview")
    style.configure("Preview.Treeview", font=(new_font, 10))

font_var.trace("w", on_font_change)

# Status bar and progress bar
status_var = tk.StringVar(value="Ready")
status_bar = ttk.Label(root, textvariable=status_var, relief='sunken', anchor='w')
status_bar.pack(side='bottom', fill='x')

progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack(side='bottom', fill='x')

root.mainloop()
