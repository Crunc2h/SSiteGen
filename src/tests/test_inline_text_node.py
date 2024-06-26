import unittest
from src.enums.text_types import TextType
from src.conversion.inline_markdown import InlineMarkdown
from src.model.text_node import TextNode


class TestInlineTextNode(unittest.TestCase):
    
    def test_text_to_text_nodes(self):
        
        case_1 = """This is **text** with an *italic* word and a `code block` and an\
![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"""
        case_2 = "**Hey bro this isn't bold as you can see it ain't clo`sed`. although you can check out this [link](asdf)"
        self.assertEqual([TextNode(text="This is ",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="text",
                                   text_type=TextType.BOLD),
                          TextNode(text=" with an ",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="italic",
                                   text_type=TextType.ITALIC),
                          TextNode(text=" word and a ",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="code block",
                                   text_type=TextType.CODE),
                          TextNode(text=" and an",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="image",
                                   text_type=TextType.IMAGE,
                                   url="https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                          TextNode(text=" and a ",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="link",
                                   text_type=TextType.LINK,
                                   url="https://boot.dev")], InlineMarkdown.text_to_text_nodes(case_1))
        self.assertRaises(ValueError, InlineMarkdown.text_to_text_nodes, case_2)

    def test_split_nodes_delimiter(self):
        
        test_nodes = [TextNode(text="This is a test node with `python ./main.sh` code inside.",
                               text_type=TextType.RAW_TEXT),
                      TextNode(text="This is just a normal text node.", 
                               text_type=TextType.RAW_TEXT),
                      TextNode(text="This text node has **bold** words in it.",
                               text_type=TextType.RAW_TEXT)]
        self.assertEqual([TextNode(text="This is a test node with ", 
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="python ./main.sh", 
                                   text_type=TextType.CODE),
                          TextNode(text=" code inside.", 
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="This is just a normal text node.", 
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="This text node has **bold** words in it.", 
                                   text_type=TextType.RAW_TEXT)], InlineMarkdown.split_nodes_delimiter(test_nodes, 
                                                                                                       "`", 
                                                                                                       TextType.CODE))
        
    def test_split_nodes_image_and_link(self):
        
        image_and_link_mixed = TextNode(text="""This is text with an\
![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)\
and\
![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) AAAAND\
[this is def link](https://google.com)""",
                                        text_type=TextType.RAW_TEXT)
        link = TextNode(text="A text with a link [test_link](https://test_link_url.com)",
                        text_type=TextType.RAW_TEXT)
        broken_image = TextNode(text="![test_image](https://unclosed_image_url.com",
                                text_type=TextType.RAW_TEXT)
        broken_link = TextNode(text="[unclosed_link_anchor(https://test_link_url.com)",
                               text_type=TextType.RAW_TEXT)
        code = TextNode(text="`python ./test.sh`",
                        text_type=TextType.CODE)
        empty = TextNode(text="", 
                         text_type=TextType.RAW_TEXT)
        null = TextNode(text=None, 
                        text_type=TextType.RAW_TEXT)
        
        case_1 = [image_and_link_mixed, null, broken_image, code, empty]
        case_2 = [image_and_link_mixed, link, null, code, broken_image]
        self.maxDiff = None
        self.assertEqual([TextNode(text="This is text with an",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="image",
                                   text_type=TextType.IMAGE,
                                   url="https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                          TextNode(text="and",
                                   text_type=TextType.RAW_TEXT),  
                          TextNode(text="another",
                                   text_type=TextType.IMAGE,
                                   url="https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
                          TextNode(text=" AAAAND[this is def link](https://google.com)",
                                   text_type=TextType.RAW_TEXT),
                          null,
                          broken_image,
                          code,
                          empty], InlineMarkdown.split_nodes_image(case_1))
        
        self.assertEqual([TextNode(text="""This is text with an\
![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)\
and\
![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) AAAAND""",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="this is def link",
                                   text_type=TextType.LINK,
                                   url="https://google.com"),
                          TextNode(text="A text with a link ",
                                   text_type=TextType.RAW_TEXT),
                          TextNode(text="test_link",
                                   text_type=TextType.LINK,
                                   url="https://test_link_url.com"),
                          null,
                          code,
                          broken_image], InlineMarkdown.split_nodes_link(case_2))

    def test_extract_markdown_images(self):
        
        test_empty = ""
        test_null = None
        test_img_text = """This is text with an\
![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)\
and\
![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"""
        self.assertRaises(TypeError, InlineMarkdown.extract_markdown_images, test_null)
        self.assertEqual([], InlineMarkdown.extract_markdown_images(test_empty)),
        self.assertEqual([("image",
                           "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                          ("another",
                           "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")],
                           InlineMarkdown.extract_markdown_images(test_img_text))
    
    def test_extract_markdown_links(self):
        
        test_empty = ""
        test_null = None
        test_link_text = """This is text with a\
[link](https://www.example.com)\
and\
[another](https://www.example.com/another)"""
        self.assertRaises(TypeError, InlineMarkdown.extract_markdown_links, test_null)
        self.assertEqual([], InlineMarkdown.extract_markdown_links(test_empty)),
        self.assertEqual([("link",
                           "https://www.example.com"),
                          ("another",
                           "https://www.example.com/another")],
                           InlineMarkdown.extract_markdown_links(test_link_text))
        
if __name__ == "__main__":
    unittest.main()