import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LibraryPage } from '@/components/LibraryPage';
import { PDFReader, PDFDocument, OutlineItem } from '@/components/PDFReader';
import { DocumentInfo } from '@/lib/api';

// Get API base URL from environment or default to adobev4 backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Library = () => {
  const [showReader, setShowReader] = useState(false);
  const [documents, setDocuments] = useState<PDFDocument[]>([]);
  const [persona, setPersona] = useState('');
  const [jobToBeDone, setJobToBeDone] = useState('');
  const navigate = useNavigate();

  const handleDocumentSelect = (selectedDocuments: DocumentInfo[], userPersona: string, userJob: string) => {
    // Convert backend DocumentInfo to frontend PDFDocument format
    const pdfDocs: PDFDocument[] = selectedDocuments.map((doc) => {
      // Convert flat outline to hierarchical structure
      const buildHierarchicalOutline = (flatOutline: any[]): OutlineItem[] => {
        const result: OutlineItem[] = [];
        const stack: OutlineItem[] = [];
        
        flatOutline.forEach((item, index) => {
          const level = parseInt(item.level.replace('H', ''));
          const outlineItem: OutlineItem = {
            id: `${doc.id}-${index}`,
            title: item.text,
            level: level,
            page: item.page,
            children: []
          };
          
          // Find the correct parent based on level hierarchy
          while (stack.length > 0 && stack[stack.length - 1].level >= level) {
            stack.pop();
          }
          
          if (stack.length === 0) {
            // Top level item
            result.push(outlineItem);
          } else {
            // Child item
            const parent = stack[stack.length - 1];
            if (!parent.children) {
              parent.children = [];
            }
            parent.children.push(outlineItem);
          }
          
          stack.push(outlineItem);
        });
        
        return result;
      };
      
      return {
        id: doc.id,
        name: doc.name,
        title: doc.title,
        url: `${API_BASE_URL}/pdf/${doc.id}`, // Use configured backend PDF endpoint
        outline: buildHierarchicalOutline(doc.outline)
      };
    });
    
    setDocuments(pdfDocs);
    setPersona(userPersona);
    setJobToBeDone(userJob);
    setShowReader(true);
  };

  const handleBack = () => {
    if (showReader) {
      setShowReader(false);
      setDocuments([]);
      setPersona('');
      setJobToBeDone('');
    } else {
      navigate('/');
    }
  };

  if (showReader && documents.length > 0) {
    return (
      <div className="relative">
        <PDFReader 
          documents={documents}
          persona={persona}
          jobToBeDone={jobToBeDone}
          onBack={handleBack}
        />
      </div>
    );
  }

  return (
    <div className="relative">
      <LibraryPage 
        onDocumentSelect={handleDocumentSelect}
        onBack={handleBack}
      />
    </div>
  );
};

export default Library;