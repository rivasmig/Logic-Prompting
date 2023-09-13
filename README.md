# Logic Prompting Technical Documentation 

## Overview 

Logic Prompting is a functional programming language designed for creating prompts in generative AI systems. It defines and integrates elements with their attributes to instruct generative models, making complex media generation simpler and more intuitive.

## Basic Constructs 

- **Elements**: Generative media is made of elements with individual attributes.
  - **Delimiter**: ⟐ surrounds each element.
  - **Example**: ⟐ ... ⟐
- **Textual Descriptions**: Describe the visual content of an element.
  - **Delimiter**: τ surrounds textual descriptions.
  - **Example**: τ a rabbit τ
- **Attributes**:
  - **Positional Data**: For image/video models, describes the position of an element.
    - **Delimiter**: χ surrounds positional data.
    - **Axis Symbol**: @ indicates an axis (x or y).
    - **Example**: χx@0y@0χ
  - **Logical Attributes**: Enables functional programming within prompts.
    - **Delimiter**: λ surrounds logical attributes.

## Reasoning 

Generative AI’s proficiency in content creation stems from its adeptness in English comprehension. To harness this, Logic Prompting uses unique symbols, ensuring clear differentiation from standard language, thus preventing interference with its core linguistic understanding.

| Symbol | Description                          | Example                   |
|--------|--------------------------------------|---------------------------|
| Emojis | Variables or function names          | 🙂 for 'smile' function   |
| δ      | Declares function definition         | δ ... δ                   |
| υ      | Uses a function                      | υ ... υ                   |
| Δ      | Function name                        | Δ ... Δ                   |
| ζ      | Parameters of a function             | ζ ... ζ... ζ              |
| Ω      | Returns what’s inside                | Ω ... Ω                   |
| α      | Refers to 'this element' or 'self'   | α                         |
| &      | Add attribute to self                | & ... &                   |
| #      | Remove or negate attribute of self   | # ... #                   |
| π      | If statement                         | π ... π                   |
| θ      | Then statement                       | θ ... θ                   |
| ε      | Else statement                       | ε ... ε                   |
| Λ      | Check or compare                     | Λ ... Λ... Λ              |
| Θ      | Search textual concept in generated media | Θ ... Θ              |
| Ψ      | Use meaning of word                  | Ψ ... Ψ                   |

## Training and UI Interface 

- **Training**: Generative AI models learn using input text and output media. Therefore with large datasets, a generative AI model could learn the logic of logic prompting.
- **UI Interface**: A user-friendly interface will be provided to simplify the creation of Logic Diffusion prompts.

### Example 

**Simple Prompt**:  
Generate an image of a man in a suit wearing a top hat next to a bunny.  
⟐ τ a man in a suit τ χx@0y@0χ ⟐|⟐ τ a top hat τ χx@0y@10χ ⟐|⟐ τ a bunny τ χx@10y@-10χ ⟐

**Logic-Incorporated Prompt**:  
To represent 'if near a car then make him happy', the syntax would look like:  
⟐ τ a man in a suit τ χx@0y@0χ λ π Λ Λ χαχ Λ χΘ car Θχ Λ Λ Ψ near Ψ Λ πθ &τ Happy τ& θ λ ⟐| ⟐ τ a top hat τ χx@0y@10χ ⟐|⟐ τ a bunny τ χx@10y@-10χ ⟐

**Function-Based Prompt**:  
Defining a function 'if near a car then happy else sad':  
⟐ λ δ Δ 📏🚗😀 Δζ 😶ζ 🚗ζΩ π Λ Λ χ😶χ Λ χ 🚗 χ Λ Λ Ψ near Ψ Λ πθ &τ Happy τ& θε &τ Sad τ& ε Ω δ λ ⟐|⟐ τ a man in a suit τ χx@0y@0χ λ υ Δ 📏🚗😀 Δζ α ζ Θ car Θ ζ υ λ ⟐|⟐ τ a top hat τ χx@0y@10χ ⟐|⟐ τ a bunny τ χx@10y@-10χ ⟐

**Function-based Color and Activity Change**:  
Define two functions: one for a dog's color based on surroundings, and one for its activity. If a dog is near a pond, it's blue and swimming; if near a ball, it's yellow and playing.  
⟐ λ δ Δ 🌊🐶🎨 Δζ 🐶ζ Ω π Λ Λ χ🐶χ Λ χΘ pond Θχ Λ Λ Ψ near Ψ Λ πθ &τ blue τ& θ ε &τ yellow τ& ε Ω δ λ ⟐ | ⟐ λ δ Δ 🐶🎭 Δζ 🐶ζ Ω π Λ Λ χ🐶χ Λ χΘ pond Θχ Λ Λ Ψ near Ψ Λ πθ &τ swimming τ& θε π Λ Λ χ🐶χ Λ χΘ ball Θχ Λ Λ Ψ near Ψ Λ πθ &τ playing τ& θ ε Ω δ λ ⟐

## Goals

The goals for this repo is to have a centralized software with the following features:
  - easy to use logic prompting ui tools for captioning and creating media (images, video, sound, and hopefully someday - video games)
 - users can turn that data into text-image pairs for generative ai training
 - users can upload that data to a cloud enviornment that has other users data as well (to easily accumulate a large amount of text-image data to train the model)
 - users can download the data stored in that cloud location
 - users can access pretrained models that have been trained by all the data uploaded to the cloud
 - users can train their own data over most generative ai models, or over a pretrained model
 - users can generate media based off these pretrained models, and logic prompting tools
 
 Other goals also include:
 - using newest research (https://arxiv.org/pdf/2307.08041.pdf) to have THIS version of the model to use. This is also favored because a system like logic prompting would benefit from an LLM generating media vs a diffusion model. Though, collecting the data is the first priority


## Conclusion 

While Logic Diffusion may seem intricate for singular image generations, it becomes increasingly powerful and useful when producing sequences or videos. It offers the capability to embed logic within media generation prompts, allowing for more intricate and nuanced generative results.

---

**Note**: This is a basic technical documentation. As Logic Diffusion develops, it may be beneficial to expand upon each section, provide more comprehensive examples, and create more in-depth user guides.
