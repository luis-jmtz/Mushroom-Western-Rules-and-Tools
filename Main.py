import pandas as pd 
import numpy as np
from equipment import *
from creatures import *
from abilities import *

import pprint
import streamlit as st

#  load data to get accurate names lists 
abilities = pd.read_csv(r"Data\Creature_abilities.tsv", sep="\t")
armor = pd.read_csv(r"Data\Armor.tsv", sep="\t")
shields = pd.read_csv(r"Data\Shields.tsv", sep="\t")
melee = pd.read_csv(r"Data\Melee.tsv", sep="\t")
projectile = pd.read_csv(r"Data\Projectile.tsv", sep="\t")
firearms = pd.read_csv(r"Data\Firearms.tsv", sep="\t")
explosives = pd.read_csv(r"Data\Explosives.tsv", sep="\t")
weapons_df = [melee, projectile,firearms]


# Streamlit App
st.set_page_config(page_title="Creature Creator", page_icon="🐲", layout="wide")

st.title("🐲 TTRPG Creature Creator")
st.markdown("Create custom monsters and NPCs for your TTRPG campaign")

# Initialize session state for creatures
if 'creatures' not in st.session_state:
    st.session_state.creatures = []

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Create Creature", "View Creatures", "Quick Templates"])

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

# Main content based on navigation
if page == "Create Creature":
    st.header("Create New Creature")
    
    with st.form("creature_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Information")
            creature_name = st.text_input("Creature Name", "Unnamed Creature")
            level = st.slider("Level", 0, 20, 1)
            size = st.selectbox("Size", 
                               ["Small (-1)", "Medium (0)", "Large (1)", "Huge (2)"],
                               index=1)
            size_map = {"Small (-1)": -1, "Medium (0)": 0, "Large (1)": 1, "Huge (2)": 2}
            size_value = size_map[size]
            
            st.subheader("Movement")
            base_speed = st.slider("Base Speed", 0, 20, 6)
            can_fly = st.checkbox("Can Fly")
            can_burrow = st.checkbox("Can Burrow")
            
            st.subheader("Action Economy")
            ap = st.slider("Action Points (AP)", 2, 10, 2)
            num_attacks = st.slider("Number of Attacks", 1, 5, 1)
            focus_points = st.slider("Focus Points", 0, 10, 0)
        
        with col2:
            st.subheader("Attributes")
            brawn = st.slider("Brawn", -5, 10, 0)
            reflex = st.slider("Reflex", -5, 10, 0)
            brains = st.slider("Brains", -5, 10, 0)
            mettle = st.slider("Mettle", -5, 10, 0)
            
            st.subheader("Equipment")
            armor_options = get_armor_options()
            selected_armor = st.selectbox("Armor", ["None"] + list(armor_options.keys()))
            
            shield_options = get_shield_options()
            selected_shield = st.selectbox("Shield", ["None"] + list(shield_options.keys()))
            
        # Weapons section
        st.subheader("Weapons")
        weapon_col1, weapon_col2, weapon_col3 = st.columns(3)
        
        weapons_to_add = []
        with weapon_col1:
            st.write("Melee Weapons")
            melee_options = get_weapon_options(0)
            selected_melee = st.multiselect("Select Melee Weapons", list(melee_options.keys()))
            weapons_to_add.extend([(0, melee_options[w]) for w in selected_melee])
        
        with weapon_col2:
            st.write("Projectile Weapons")
            projectile_options = get_weapon_options(1)
            selected_projectile = st.multiselect("Select Projectile Weapons", list(projectile_options.keys()))
            weapons_to_add.extend([(1, projectile_options[w]) for w in selected_projectile])
        
        with weapon_col3:
            st.write("Firearms")
            firearm_options = get_weapon_options(2)
            selected_firearms = st.multiselect("Select Firearms", list(firearm_options.keys()))
            weapons_to_add.extend([(2, firearm_options[w]) for w in selected_firearms])
        
        # Explosives section
        st.subheader("Explosives")
        explosive_col1, explosive_col2 = st.columns(2)
        
        with explosive_col1:
            explosive_options = get_explosive_options()
            selected_explosives = st.multiselect("Select Explosives", list(explosive_options.keys()))
        
        with explosive_col2:
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
            
            # Store creature with name and stats
            creature_data = {
                'name': creature_name,
                'creature': creature,
                'difficulty': difficulty,
                'ac': creature.ac,
                'luck': creature.luck,
                'dpr': creature.dpr,
                'attack_bonus': creature.attack_bonus,
                'save_dc': creature.save_dc
            }
            
            st.session_state.creatures.append(creature_data)
            st.success(f"Creature '{creature_name}' created successfully!")
            
            # Display creature summary
            st.subheader("Creature Summary")
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.write(f"**Level:** {creature.level}")
                st.write(f"**Size:** {size}")
                st.write(f"**Speed:** {creature.speed} ft")
                if creature.canFly:
                    st.write("**Can Fly:** Yes")
                if creature.canBurrow:
                    st.write("**Can Burrow:** Yes")
                
                st.write(f"**Action Points:** {creature.ap}")
                st.write(f"**Number of Attacks:** {creature.num_attacks}")
                st.write(f"**Focus Points:** {creature.focus_points}")
            
            with summary_col2:
                st.write(f"**AC:** {creature.ac}")
                st.write(f"**Luck (HP):** {creature.luck}")
                st.write(f"**Attack Bonus:** +{creature.attack_bonus}")
                st.write(f"**Save DC:** {creature.save_dc}")
                st.write(f"**DPR:** {creature.dpr:.2f}")
                st.write(f"**Difficulty:** {difficulty:.2f}")

elif page == "View Creatures":
    st.header("Created Creatures")
    
    if not st.session_state.creatures:
        st.info("No creatures created yet. Go to 'Create Creature' to make your first creature!")
    else:
        for i, creature_data in enumerate(st.session_state.creatures):
            with st.expander(f"{creature_data['name']} (Level {creature_data['creature'].level}, Difficulty: {creature_data['difficulty']:.2f})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("Core Stats")
                    st.write(f"**Level:** {creature_data['creature'].level}")
                    st.write(f"**Size:** {creature_data['creature'].size}")
                    st.write(f"**Speed:** {creature_data['creature'].speed} ft")
                    st.write(f"**Action Points:** {creature_data['creature'].ap}")
                    st.write(f"**Number of Attacks:** {creature_data['creature'].num_attacks}")
                
                with col2:
                    st.subheader("Combat Stats")
                    st.write(f"**AC:** {creature_data['ac']}")
                    st.write(f"**Luck (HP):** {creature_data['luck']}")
                    st.write(f"**Attack Bonus:** +{creature_data['attack_bonus']}")
                    st.write(f"**Save DC:** {creature_data['save_dc']}")
                    st.write(f"**DPR:** {creature_data['dpr']:.2f}")
                
                with col3:
                    st.subheader("Attributes")
                    st.write(f"**Brawn:** {creature_data['creature'].brawn}")
                    st.write(f"**Reflex:** {creature_data['creature'].reflex}")
                    st.write(f"**Brains:** {creature_data['creature'].brains}")
                    st.write(f"**Mettle:** {creature_data['creature'].mettle}")
                    st.write(f"**Prime:** {creature_data['creature'].prime}")
                
                # Equipment and Abilities
                col4, col5 = st.columns(2)
                
                with col4:
                    st.subheader("Equipment")
                    if creature_data['creature'].armor:
                        st.write(f"**Armor:** {creature_data['creature'].armor.name}")
                    if creature_data['creature'].shield:
                        st.write(f"**Shield:** {creature_data['creature'].shield.name}")
                    
                    if creature_data['creature'].weapons:
                        st.write("**Weapons:**")
                        for weapon in creature_data['creature'].weapons:
                            st.write(f"- {weapon.name} (Dmg: {weapon.dmg})")
                    
                    if creature_data['creature'].explosives:
                        st.write("**Explosives:**")
                        for explosive, count in creature_data['creature'].explosives:
                            st.write(f"- {explosive.name} x{count} (Dmg: {explosive.dmg}, Radius: {explosive.radius})")
                
                with col5:
                    st.subheader("Abilities")
                    if creature_data['creature'].abilties:
                        for ability in creature_data['creature'].abilties:
                            st.write(f"- **{ability.name}**: {ability.description} (Type: {ability.type}, Points: {ability.points})")
                    else:
                        st.write("No abilities")
                
                # Delete button
                if st.button(f"Delete {creature_data['name']}", key=f"delete_{i}"):
                    st.session_state.creatures.pop(i)
                    st.rerun()

elif page == "Quick Templates":
    st.header("Quick Creature Templates")
    
    template_col1, template_col2, template_col3 = st.columns(3)
    
    with template_col1:
        st.subheader("Low-Level Threat")
        if st.button("Create Bandit"):
            bandit = Creature()
            bandit.level = 1
            bandit.brawn = 2
            bandit.reflex = 1
            bandit.brains = -1
            bandit.mettle = 0
            bandit.add_armor(1)  # Assuming 1 is leather armor
            bandit.add_weapon(0, 1)  # Assuming type 0, id 1 is a dagger
            
            bandit.calc_bonuses()
            bandit.calc_ac()
            bandit.calc_dpr()
            difficulty = bandit.calculate_difficulty()
            
            creature_data = {
                'name': "Bandit",
                'creature': bandit,
                'difficulty': difficulty,
                'ac': bandit.ac,
                'luck': bandit.luck,
                'dpr': bandit.dpr,
                'attack_bonus': bandit.attack_bonus,
                'save_dc': bandit.save_dc
            }
            
            st.session_state.creatures.append(creature_data)
            st.success("Bandit template created!")
    
    with template_col2:
        st.subheader("Mid-Level Threat")
        if st.button("Create Veteran Warrior"):
            warrior = Creature()
            warrior.level = 5
            warrior.brawn = 4
            warrior.reflex = 2
            warrior.brains = 0
            warrior.mettle = 2
            warrior.add_armor(3)  # Assuming 3 is chainmail
            warrior.add_weapon(0, 5)  # Assuming type 0, id 5 is a longsword
            warrior.add_ability(1)  # Assuming id 1 is a combat ability
            
            warrior.calc_bonuses()
            warrior.calc_ac()
            warrior.calc_dpr()
            difficulty = warrior.calculate_difficulty()
            
            creature_data = {
                'name': "Veteran Warrior",
                'creature': warrior,
                'difficulty': difficulty,
                'ac': warrior.ac,
                'luck': warrior.luck,
                'dpr': warrior.dpr,
                'attack_bonus': warrior.attack_bonus,
                'save_dc': warrior.save_dc
            }
            
            st.session_state.creatures.append(creature_data)
            st.success("Veteran Warrior template created!")
    
    with template_col3:
        st.subheader("High-Level Threat")
        if st.button("Create Elite Guardian"):
            guardian = Creature()
            guardian.level = 10
            guardian.brawn = 6
            guardian.reflex = 3
            guardian.brains = 1
            guardian.mettle = 4
            guardian.size = 1  # Large
            guardian.add_armor(5)  # Assuming 5 is plate armor
            guardian.add_shield(1)  # Assuming 1 is a heavy shield
            guardian.add_weapon(0, 8)  # Assuming type 0, id 8 is a greatsword
            guardian.add_ability(1)
            guardian.add_ability(2)  # Assuming id 2 is another ability
            
            guardian.calc_bonuses()
            guardian.calc_ac()
            guardian.calc_dpr()
            difficulty = guardian.calculate_difficulty()
            
            creature_data = {
                'name': "Elite Guardian",
                'creature': guardian,
                'difficulty': difficulty,
                'ac': guardian.ac,
                'luck': guardian.luck,
                'dpr': guardian.dpr,
                'attack_bonus': guardian.attack_bonus,
                'save_dc': guardian.save_dc
            }
            
            st.session_state.creatures.append(creature_data)
            st.success("Elite Guardian template created!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "This creature creator uses your custom TTRPG system to generate "
    "balanced monsters and NPCs with calculated stats and difficulty ratings."
)



# bandit = Creature()
# bandit.brawn = 3
# bandit.reflex = 1
# bandit.brains = -2
# bandit.mettle = 0

# bandit.add_armor(1)
# bandit.add_weapon(2,6)
# bandit.add_weapon(0,9)

# bandit.calc_dpr()
# print(f"DPR: {bandit.dpr}")

# bandit.add_ability(1)

# diff = bandit.calculate_difficulty()

# print(diff)

# print(bandit.abilties[0].name)

# bandit.add_ability(1)

# diff = bandit.calculate_difficulty()

# print(diff)