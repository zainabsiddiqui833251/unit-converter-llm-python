import streamlit as st
from deep_translator import GoogleTranslator
from pint import UnitRegistry

# Initialize Pint unit registry
ureg = UnitRegistry()

def translate_to_english(text):
    """Translates any language to English using Deep Translator."""
    return GoogleTranslator(source='auto', target='en').translate(text)

def convert_units(query):
    """Performs unit conversion using Pint."""
    try:
        words = query.lower().split()
        
        # Find numeric value
        amount = next((float(word) for word in words if word.replace('.', '', 1).isdigit()), None)
        if amount is None:
            return "Error: No numeric value found!"
        
        # Identify possible unit words
        potential_units = [word for word in words if word.isalpha()]
        
        # Validate units using Pint
        from_unit, to_unit = None, None
        for word in potential_units:
            try:
                parsed_unit = ureg.parse_units(word)
                if not from_unit:
                    from_unit = parsed_unit
                else:
                    to_unit = parsed_unit
                    break
            except Exception:
                continue  # Skip unrecognized words
        
        if not from_unit or not to_unit:
            return "Error: Units not recognized!"
        
        # Perform conversion
        result = (amount * from_unit).to(to_unit)
        return f"{amount} {from_unit} = {result}"
    
    except Exception as e:
        return f"Error: {e}"

def main():
    st.set_page_config(page_title="Free Unit Converter", page_icon="🔄", layout="centered")

    st.title("🌍 Free Universal Unit Converter")
    st.subheader("Convert any unit in any language!")

    user_input = st.text_input("Enter your conversion query (any language):", 
                               placeholder="e.g., Convert 5 kilogram to pounds")
    
    if st.button("Convert 🔄"):
        if user_input:
            # Translate to English for better understanding
            user_input = translate_to_english(user_input)

            # Perform unit conversion
            result = convert_units(user_input)

            # Display the result
            st.success(result)
        else:
            st.warning("Please enter a conversion query!")

if __name__ == "__main__":
    main()
