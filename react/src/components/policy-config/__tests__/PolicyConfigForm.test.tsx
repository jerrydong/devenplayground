import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PolicyConfigForm } from '../';
import type { PolicyConfigFormData } from '../types';

// Mock data
const mockCities = ['北京', '上海', '广州', '深圳'];
const mockVersions = ['11.0.0', '11.1.0', '11.2.0', '11.2.8', '12.0.0'];

// Helper function to render the component
const renderPolicyConfigForm = () => {
  return render(<PolicyConfigForm />);
};

describe('PolicyConfigForm', () => {
  // Basic Strategy Tests
  describe('Basic Strategy Configuration', () => {
    test('renders all basic strategy sections', () => {
      renderPolicyConfigForm();
      
      // Check section headings
      expect(screen.getByText('基础策略')).toBeInTheDocument();
      expect(screen.getByText('接单前')).toBeInTheDocument();
      expect(screen.getByText('待取货')).toBeInTheDocument();
      expect(screen.getByText('待送达')).toBeInTheDocument();
    });

    test('validates required fields in basic strategy', async () => {
      renderPolicyConfigForm();
      
      // Try to submit without filling required fields
      const submitButton = screen.getByText('确定');
      fireEvent.click(submitButton);

      // Check for validation messages
      await waitFor(() => {
        expect(screen.getAllByText('主标题内容类型不能为空')).toHaveLength(3);
        expect(screen.getAllByText('副标题内容类型不能为空')).toHaveLength(3);
      });
    });
  });

  // Display Range Tests
  describe('Display Range Configuration', () => {
    test('switches between all and gray modes', () => {
      renderPolicyConfigForm();
      
      const grayRadio = screen.getByLabelText('灰度');
      const allRadio = screen.getByLabelText('全量');

      fireEvent.click(grayRadio);
      expect(screen.getByText('添加')).toBeInTheDocument();

      fireEvent.click(allRadio);
      expect(screen.queryByText('添加')).not.toBeInTheDocument();
    });

    test('handles city selection and filtering', async () => {
      renderPolicyConfigForm();
      
      // Switch to gray mode
      fireEvent.click(screen.getByLabelText('灰度'));

      // Select city type
      const typeSelect = screen.getByRole('combobox', { name: /类型/ });
      fireEvent.change(typeSelect, { target: { value: '加盟' } });

      // Select cities
      const citySelect = screen.getByRole('combobox', { name: /城市/ });
      fireEvent.change(citySelect, { target: { value: ['北京', '上海'] } });

      // Add cities
      const addButton = screen.getByText('添加');
      fireEvent.click(addButton);

      // Verify tags are created
      expect(screen.getByText('加盟-北京')).toBeInTheDocument();
      expect(screen.getByText('加盟-上海')).toBeInTheDocument();
    });
  });

  // System Version Tests
  describe('System Version Configuration', () => {
    test('handles version logic selection', async () => {
      renderPolicyConfigForm();
      
      // Switch to gray mode
      fireEvent.click(screen.getByLabelText('灰度'));

      // Select logic
      const logicSelect = screen.getByRole('combobox', { name: /逻辑/ });
      fireEvent.change(logicSelect, { target: { value: 'eq' } });

      // Verify multiple selection is enabled for 'eq' logic
      const versionSelect = screen.getByRole('combobox', { name: /版本/ });
      expect(versionSelect).toHaveAttribute('mode', 'multiple');

      // Change to other logic
      fireEvent.change(logicSelect, { target: { value: 'gt' } });
      expect(versionSelect).not.toHaveAttribute('mode', 'multiple');
    });
  });

  // Suffix Restriction Tests
  describe('Suffix Restriction Configuration', () => {
    test('handles suffix type and digit selection', async () => {
      renderPolicyConfigForm();
      
      // Switch to gray mode
      fireEvent.click(screen.getByLabelText('灰度'));

      // Select suffix type
      const suffixTypeSelect = screen.getByRole('combobox', { name: /类型/ });
      fireEvent.change(suffixTypeSelect, { target: { value: 'phone' } });

      // Select digits
      const digitSelect = screen.getByRole('combobox', { name: /尾号/ });
      fireEvent.change(digitSelect, { target: { value: ['0', '1', '2'] } });

      // Verify selections are reflected
      expect(screen.getByText('0')).toBeInTheDocument();
      expect(screen.getByText('1')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument();
    });
  });

  // Form Submission Test
  describe('Form Submission', () => {
    test('submits form with complete data', async () => {
      const { container } = renderPolicyConfigForm();
      
      // Fill in all required fields
      // Basic Strategy
      const mainTitleRadios = screen.getAllByLabelText('脱敏后地址');
      mainTitleRadios.forEach(radio => fireEvent.click(radio));

      const subTitleRadios = screen.getAllByLabelText('结构化地址');
      subTitleRadios.forEach(radio => fireEvent.click(radio));

      // Submit form
      const submitButton = screen.getByText('确定');
      fireEvent.click(submitButton);

      // Verify no validation errors
      await waitFor(() => {
        expect(screen.queryByText(/不能为空/)).not.toBeInTheDocument();
      });
    });
  });
});
