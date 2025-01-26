    if input_keywords is None:

        generator = OaiContentGenerator(model_name=generation_model)
        
        # Generate first set of keywords using AI
        ai_keywords1 = generator.GenerateKeywords(topic=topic)
        if not ai_keywords1 or not isinstance(ai_keywords1, list):
            print("Error: No keywords generated.")
            ai_keywords1 = []
        for i,kw_sublist in enumerate(ai_keywords1):
            ai_keywords1[i] = [kw.strip() for kw in kw_sublist]
        

        # Generate second set of keywords using web scraping
        scraper = GoogleScraper()
        keywords = scraper.get_keywords_from_google(topic, num_results=50, num_keywords=20)
        ai_keywords2 = generator.GenerateKeywordsFromSearchResults(search_results=keywords, topic=topic)
        if not ai_keywords2 or not isinstance(ai_keywords2, list):
            print("Error: No keywords generated.")
            ai_keywords1 = []
        for i,kw_sublist in enumerate(ai_keywords2):
            ai_keywords2[i] = [kw.strip() for kw in kw_sublist]
        
        # Combine and shuffle keywords
        final_keywords = ai_keywords1 + ai_keywords2
        random.shuffle(final_keywords)
        final_keywords = final_keywords[:3]
    else:
        final_keywords = input_keywords


    # PHASE 2: CONTENT GENERATION
    # Generate blog posts, titles, and meta descriptions for each keyword
    contentgen = ContentGeneration()
    generated_posts, generated_titles, generated_metadescriptions = contentgen.Posts_Titles_Metadescriptions_Generator (generation_model, final_keywords)
    '''generated_posts = []
    generated_titles = []
    generated_metadescriptions = []

    for keywords in final_keywords:
        post = generator.GenerateBlogPost(keyword=keywords)
        title = generator.GeneratePostTitle(blog_text=post, keyword=keywords)
        metadescription = generator.GeneratePostMetaDescription(blog_text=post, blog_title=title, keyword=keywords)
        #post = title + "\n" + metadescription + "\n" + post
        generated_posts.append(post)
        generated_titles.append(title)
        generated_metadescriptions.append(metadescription)'''

    # PHASE 3: SEO OPTIMIZATION
    # Analyze and improve each post for SEO
    seo_model = os.getenv("seo_model", "gpt-4o-mini") # Model name for AI content generation
    

    fixer = SEOFixer()
    seo_optimized_posts, seo_optimized_titles, seo_optimized_metadescriptions = fixer.fixSEO(seo_model=seo_model, generated_posts=generated_posts, generated_titles=generated_titles, generated_metadescriptions=generated_metadescriptions, final_keywords=final_keywords)
    '''analyzer = SEOAnalyzer()
    fixer = OaiSeoSpecialist(model_name=seo_model)
    seo_optimized_posts = []
    seo_optimized_titles = []
    seo_optimized_metadescriptions = []

    for i, post in enumerate(generated_posts):
        existing_posts = generated_posts[:i]+generated_posts[i+1:]
        existing_titles = generated_titles[:i]+generated_titles[i+1:]
        existing_metadescriptions = generated_metadescriptions[:i]+generated_metadescriptions[i+1:]

        corrections_post = analyzer.generate_report_post(
                                        content=post,
                                        target_keywords=final_keywords[i], 
                                        existing_contents=existing_posts
                                    )
        corrections_title = analyzer.generate_report_title(
                                        title=generated_titles[i],
                                        target_keywords=final_keywords[i],
                                        existing_contents=existing_titles
                                    )
        corrections_metadescription = analyzer.generate_report_meta_description(
                                        meta_description=generated_metadescriptions[i],
                                        target_keywords=final_keywords[i],
                                        existing_contents=existing_metadescriptions
                                    )
        
        improved_post = fixer.FixBlogPost(post, corrections_post)
        improved_title = fixer.FixBlogTitle(generated_titles[i], corrections_title)
        improved_metadescription = fixer.FixMetaDescription(generated_metadescriptions[i], corrections_metadescription)
        seo_optimized_posts.append(improved_post)
        seo_optimized_titles.append(improved_title)
        seo_optimized_metadescriptions.append(improved_metadescription)'''
