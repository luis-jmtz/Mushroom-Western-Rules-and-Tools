import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
from abilities import *

import pprint
import streamlit as st

# Load data to get accurate names lists 
abilities_df = pd.read_csv(r"Data\Creature_abilities.tsv", sep="\t")
armor_df = pd.read_csv(r"Data\Armor.tsv", sep="\t")
shields_df = pd.read_csv(r"Data\Shields.tsv", sep="\t")
melee_df = pd.read_csv(r"Data\Melee.tsv", sep="\t")
projectile_df = pd.read_csv(r"Data\Projectile.tsv", sep="\t")
firearms_df = pd.read_csv(r"Data\Firearms.tsv", sep="\t")
explosives_df = pd.read_csv(r"Data\Explosives.tsv", sep="\t")
weapons_df_list = [melee_df, projectile_df, firearms_df]

# Helper functions for dropdowns
def get_armor_options():
    return {f"{row['name']} (AC: {row['AC']})": row['id'] for _, row in armor_df.iterrows()}

def get_shield_options():
    return {f"{row['name']} (AC: {row['ac']})": row['id'] for _, row in shields_df.iterrows()}

def get_weapon_options(weapon_type):
    weapon_names = {
        0: "Melee",
        1: "Projectile", 
        2: "Firearms"
    }
    df = weapons_df_list[weapon_type]
    return {f"{row['name']} (Dmg: {row['dmg']})": row['id'] for _, row in df.iterrows()}

def get_explosive_options():
    return {f"{row['name']} (Dmg: {row['dmg']}, Radius: {row['radius']})": row['id'] for _, row in explosives_df.iterrows()}

def get_ability_options():
    return {f"{row['name']} (Type: {row['type']}, Points: {row['points']})": row['id'] for _, row in abilities_df.iterrows()}

# Streamlit App
st.title("Creature Creator")

st.header("Create New Creature")

with st.form("creature_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        creature_name = st.text_input("Creature Name", "Unnamed Creature")
        level = st.number_input("Level", 0, 20, 1)
        size = st.selectbox("Size", 
                           ["Small (-1)", "Medium (0)", "Large (1)", "Huge (2)"],
                           index=1)
        size_map = {"Small (-1)": -1, "Medium (0)": 0, "Large (1)": 1, "Huge (2)": 2}
        size_value = size_map[size]
        
        st.subheader("Movement")
        base_speed = st.number_input("Base Speed", 0, 20, 6)
        can_fly = st.checkbox("Can Fly")
        can_burrow = st.checkbox("Can Burrow")
        
        st.subheader("Action Economy")
        ap = st.number_input("AP", 2, 10, 2)
        num_attacks = st.number_input("Number of Attacks", 1, 5, 1)
        focus_points = st.number_input("FP", 0, 10, 0)
    
    with col2:
        st.subheader("Attributes")
        brawn = st.number_input("Brawn", -5, 10, 0)
        reflex = st.number_input("Reflex", -5, 10, 0)
        brains = st.number_input("Brains", -5, 10, 0)
        mettle = st.number_input("Mettle", -5, 10, 0)
        
        st.subheader("Equipment")
        armor_options = get_armor_options()
        selected_armor = st.selectbox("Armor", ["None"] + list(armor_options.keys()))
        
        shield_options = get_shield_options()
        selected_shield = st.selectbox("Shield", ["None"] + list(shield_options.keys()))
        
    # Weapons section
    st.subheader("Weapons")
    
    weapons_to_add = []
    
    st.write("Melee Weapons")
    melee_options = get_weapon_options(0)
    selected_melee = st.multiselect("Select Melee Weapons", list(melee_options.keys()))
    weapons_to_add.extend([(0, melee_options[w]) for w in selected_melee])
    
    st.write("Projectile Weapons")
    projectile_options = get_weapon_options(1)
    selected_projectile = st.multiselect("Select Projectile Weapons", list(projectile_options.keys()))
    weapons_to_add.extend([(1, projectile_options[w]) for w in selected_projectile])
    
    st.write("Firearms")
    firearm_options = get_weapon_options(2)
    selected_firearms = st.multiselect("Select Firearms", list(firearm_options.keys()))
    weapons_to_add.extend([(2, firearm_options[w]) for w in selected_firearms])
    
    # Explosives section
    st.subheader("Explosives")
    
    explosive_options = get_explosive_options()
    selected_explosives = st.multiselect("Select Explosives", list(explosive_options.keys()))
    
    explosive_counts = {}
    for explosive in selected_explosives:
        count = st.number_input(f"Count for {explosive}", 1, 100, 1, key=f"exp_{explosive}")
        explosive_counts[explosive_options[explosive]] = count
    
    # Abilities section
    st.subheader("Abilities")
    ability_options = get_ability_options()
    selected_abilities = st.multiselect("Select Abilities", list(ability_options.keys()))
    
    # Submit button
    submitted = st.form_submit_button("Create Creature")
    
    if submitted:
        # Create the creature
        creature = Creature()
        creature.level = level
        creature.size = size_value
        creature.base_speed = base_speed
        creature.canFly = can_fly
        creature.canBurrow = can_burrow
        creature.ap = ap
        creature.num_attacks = num_attacks
        creature.focus_points = focus_points
        
        # Set attributes
        creature.brawn = brawn
        creature.reflex = reflex
        creature.brains = brains
        creature.mettle = mettle
        
        # Add equipment
        if selected_armor != "None":
            creature.add_armor(armor_options[selected_armor])
        
        if selected_shield != "None":
            creature.add_shield(shield_options[selected_shield])
        
        # Add weapons
        for weapon_type, weapon_id in weapons_to_add:
            creature.add_weapon(weapon_type, weapon_id)
        
        # Add explosives
        for explosive_id, count in explosive_counts.items():
            creature.add_explosives(explosive_id, count)
        
        # Add abilities
        for ability in selected_abilities:
            creature.add_ability(ability_options[ability])
        
        # Calculate stats
        creature.calc_bonuses()
        creature.calc_ac()
        creature.calc_dpr()
        difficulty = creature.calculate_difficulty()
        
        # Display creature summary
        st.subheader("Creature Summary")
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.write(f"Level: {creature.level}")
            st.write(f"Size: {size}")
            st.write(f"Speed: {creature.speed}")
            if creature.canFly:
                st.write("Can Fly: Yes")
            if creature.canBurrow:
                st.write("Can Burrow: Yes")
            
            st.write(f"AP: {creature.ap}")
            st.write(f"Number of Attacks: {creature.num_attacks}")
            st.write(f"FP: {creature.focus_points}")
        
        with summary_col2:
            st.write(f"AC: {creature.ac}")
            st.write(f"Luck (HP): {creature.luck}")
            st.write(f"Attack Bonus: +{creature.attack_bonus}")
            st.write(f"Save DC: {creature.save_dc}")
            st.write(f"DPR: {creature.dpr:.2f}")
            st.write(f"Difficulty: {difficulty:.2f}")
        
        # Equipment and Abilities
        col4, col5 = st.columns(2)
        
        with col4:
            st.subheader("Equipment")
            if creature.armor:
                st.write(f"Armor: {creature.armor.name}")
            if creature.shield:
                st.write(f"Shield: {creature.shield.name}")
            
            if creature.weapons:
                st.write("Weapons:")
                for weapon in creature.weapons:
                    st.write(f"- {weapon.name} (Dmg: {weapon.dmg})")
            
            if creature.explosives:
                st.write("Explosives:")
                for explosive, count in creature.explosives:
                    st.write(f"- {explosive.name} x{count} (Dmg: {explosive.dmg}, Radius: {explosive.radius})")
        
        with col5:
            st.subheader("Abilities")
            if creature.abilties:
                for ability in creature.abilties:
                    st.write(f"- {ability.name}: {ability.description} (Type: {ability.type}, Points: {ability.points})")
            else:
                st.write("No abilities")