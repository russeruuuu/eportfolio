from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
notes={
'WEEK 02':('Language, understood.','Introduction to NLP Concepts','Exploring how computers interpret human language through Microsoft Learn and language playground activities.','Natural language processing',['NLP','Microsoft Learn'],'I learned how text can be processed and analyzed using different NLP techniques. The activity also introduced tools that can identify important information in text and generate responses based on user input.','Understanding NLP can help me develop smarter systems that interact with users more effectively.','One challenge I faced was understanding how computers interpret human language, since people often use words in different ways. I worked through the concepts by reviewing the lessons and completing the hands-on activities.'),
'WEEK 03':('Learning from examples.','Deep Learning and Neural Networks','Training a customer feedback classifier, testing new examples, and examining the effect of better training data.','Text classification',['Neural networks','Classification'],'I trained a model using examples of customer feedback about mobile phones. The model learned to identify whether a message was a compliment, a complaint, or a request for urgent support.','Text classification can organize customer feedback and help teams identify urgent concerns.','The model depended heavily on the examples it was trained with. Limited training data made it harder to recognize different ways people express the same message. Adding examples helped me understand the importance of data quality.'),
'WEEK 04':('Small changes. Better models.','Neural Network Training','Comparing hyperparameters, training logs, and model evaluation in a customer feedback classification experiment.','Model training',['TensorFlow','Hyperparameters'],'I explored how changing model settings, called hyperparameters, can affect the performance of a machine learning model.','Understanding model training helps me evaluate prediction quality and recognize overfitting and underfitting.','I initially thought that adjusting settings alone would significantly improve results. The experiments helped me understand the importance of balancing model design, training settings, and data quality.'),
'WEEK 06':('Putting knowledge to work.','Preliminary Examination','A photographic record of the preliminary examination.','Assessment',['Exam'],None,None,None),
'WEEK 08':('Answers with a source.','Building and Evaluating a RAG Chatbot','An Arcane lore chatbot that retrieves information from a curated knowledge base before generating an answer.','Retrieval-augmented generation',['RAG','Arcane'],'I learned how different AI tools work together to retrieve information, process data, and generate responses grounded in a set of documents.','Connecting a chatbot to trusted information can improve reliability and reduce unsupported answers.','Understanding how embeddings, vector databases, and retrieval systems work together was a challenge. Studying the pipeline and observing its answers helped me understand how retrieved information supports generation.'),
'WEEK 10':('From idea to proposal.','DecisionThree Project Proposal','The initial IEEE proposal and presentation for the DecisionThree group project.','Project planning',['Proposal','DecisionThree'],None,None,None),
'WEEK 11':('Refining the direction.','Updated Project Proposal','The revised DecisionThree proposal and presentation, preserved alongside the initial project direction.','Project development',['Proposal','Revision'],None,None,None),
'WEEK 12':('Connecting the concepts.','Midterm Examination','A photographic record of the midterm examination.','Assessment',['Exam'],None,None,None),
'WEEK 14':('The right context.','Chunk Size and Overlap','Initial document preparation and vector indexing for a JRU program inquiry chatbot, using the IT and Business Analytics source.','Document indexing',['Chunking','Embeddings'],None,None,None),
'WEEK 15':('Testing the retrieval.','Finding the Best Chunk Configuration','A follow-up experiment comparing chunk configurations, with a notebook, configuration workbook, and supporting reports.','Retrieval experiments',['RAG','Evaluation'],None,None,None),
'WEEK 16':('Measuring the tradeoffs.','Optimization and GPU Testing','The DecisionThree RAG experiment report, results workbook, notebook, and experiment data.','Performance evaluation',['Optimization','GPU'],None,None,None),
'WEEK 18':('Bringing it all together.','DecisionThree Final Project','The final group project brings together a source-grounded chatbot, an IEEE report, evaluation results, and reproducible project inputs.','Final project',['DecisionThree','RAG'],None,None,None),
}
content=json.loads((root/'content/reflections.json').read_text())
items=[]
for term in ['PRELIMS','MIDTERMS','FINALS']:
 for folder in sorted((root/'ACTIVITIES'/term).iterdir()):
  if not folder.is_dir():continue
  files=[p for p in sorted(folder.iterdir()) if p.is_file() and not p.name.startswith('.')]
  key=next((k for k in notes if folder.name.startswith(k)),None)
  week=folder.name.split()[1]
  if not key:
   extra=content.get(week)
   if not extra:continue
   n=('',extra['title'],extra['summary'],extra['topic'],extra['tags'],None,None,None)
  else:
   n=notes[key];week=key.split()[-1]
  items.append(dict(id=f'week-{week}',week=week,term=term.title(),eyebrow=n[0],title=n[1],summary=n[2],topic=n[3],tags=n[4],skills=n[5],importance=n[6],reflection=n[7],files=[dict(name=p.name,path=p.relative_to(root).as_posix(),type=p.suffix[1:].upper(),size=p.stat().st_size) for p in files]))
for item in items:
 extra=content.get(item['week'],{})
 for field in ['skills','importance','reflection','links','contributions']:
  if field in extra:item[field]=extra[field]
takeaways=json.loads((root/'content/takeaways.json').read_text())
(root/'assets/takeaways.js').write_text('window.PORTFOLIO_TAKEAWAYS = '+json.dumps(takeaways,ensure_ascii=False,indent=2)+';\n')
(root/'assets/catalog.js').write_text('window.PORTFOLIO_ACTIVITIES = '+json.dumps(items,ensure_ascii=False,indent=2)+';\n')
print(f'Catalog: {len(items)} activities, {sum(len(i["files"]) for i in items)} artifacts')
