from textnode import TextNode  # import our object
from textnode import TextType  # import the TextType Enum

print("hello world")

def main():
    # create dummy object
    dummy_object = TextNode("this is a text node", TextType.BOLD, "https://www.boot.dev")
    # Must use Enum for bold, as simply "bold" won't work
    print(dummy_object)

# Need this to run!
if __name__ == "__main__":
    main()