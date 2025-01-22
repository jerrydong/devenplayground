import React, { useState } from 'react';
import { Form, Radio, Select, Button, Tag, Space } from 'antd';
import type { RadioChangeEvent } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import type { 
  DisplayMode, 
  VersionLogic,
  PlatformType,
  SuffixType,
  PolicyConfigFormData,
  VersionConfig 
} from './types';

const { Option } = Select;

const PolicyConfigForm: React.FC = () => {
  const [form] = Form.useForm<PolicyConfigFormData>();
  
  // State for conditional rendering
  const [displayMode, setDisplayMode] = useState<DisplayMode>('all');
  const [versionMode, setVersionMode] = useState<DisplayMode>('all');
  const [suffixMode, setSuffixMode] = useState<DisplayMode>('all');
  
  // Mock data - to be replaced with real data
  const mockCities = ['北京', '上海', '广州', '深圳'];
  const mockVersions = ['11.0.0', '11.1.0', '11.2.0', '11.2.8', '12.0.0'];
  const mockSuffixTypes: SuffixType[] = ['phone', 'riderId', 'meiTuanId'];
  const mockDigits = Array.from({ length: 10 }, (_, i) => i); // 0-9

  // State for city selection
  const [cityRows, setCityRows] = useState<Array<{ key: number; type: string; cities: string[] }>>([
    { key: 1, type: '加盟', cities: [] }
  ]);
  const [selectedCities, setSelectedCities] = useState<string[]>([]);
  const [nextKey, setNextKey] = useState(2);

  // State for version configuration
  const [versionConfigs, setVersionConfigs] = useState<VersionConfig[]>([
    { platform: 'android', logic: 'eq', versions: [] },
    { platform: 'ios', logic: 'eq', versions: [] }
  ]);

  // State for suffix configuration
  const [selectedSuffixType, setSelectedSuffixType] = useState<SuffixType>('phone');
  const [selectedDigits, setSelectedDigits] = useState<number[]>([]);

  const handleDisplayModeChange = (e: RadioChangeEvent) => {
    setDisplayMode(e.target.value);
  };
  
  const handleVersionModeChange = (e: RadioChangeEvent) => {
    setVersionMode(e.target.value);
  };
  
  const handleSuffixModeChange = (e: RadioChangeEvent) => {
    setSuffixMode(e.target.value);
  };

  // City selection handlers
  const addCityRow = () => {
    setCityRows([...cityRows, { key: nextKey, type: '加盟', cities: [] }]);
    setNextKey(nextKey + 1);
  };

  const removeCityRow = (key: number) => {
    setCityRows(cityRows.filter(row => row.key !== key));
  };

  const handleTypeChange = (key: number, value: string) => {
    setCityRows(cityRows.map(row => 
      row.key === key ? { ...row, type: value } : row
    ));
  };

  const handleCityChange = (key: number, values: string[]) => {
    setCityRows(cityRows.map(row => 
      row.key === key ? { ...row, cities: values } : row
    ));
  };

  const addSelectedCities = (key: number) => {
    const row = cityRows.find(r => r.key === key);
    if (row && row.cities.length > 0) {
      const newCities = row.cities.map(city => `${row.type}-${city}`);
      setSelectedCities([...selectedCities, ...newCities]);
    }
  };

  const removeSelectedCity = (city: string) => {
    setSelectedCities(selectedCities.filter(c => c !== city));
  };

  // Version configuration handlers
  const handleVersionLogicChange = (platform: PlatformType, logic: VersionLogic) => {
    setVersionConfigs(configs => 
      configs.map(config => 
        config.platform === platform 
          ? { ...config, logic, versions: logic === 'eq' ? config.versions : config.versions.slice(0, 1) }
          : config
      )
    );
  };

  const handleVersionSelect = (platform: PlatformType, versions: string[]) => {
    setVersionConfigs(configs =>
      configs.map(config =>
        config.platform === platform ? { ...config, versions } : config
      )
    );
  };

  const renderContentTypeRadioGroup = (fieldName: string) => (
    <Form.Item noStyle>
      <Radio.Group>
        <Radio value="desensitized">脱敏后地址</Radio>
        <Radio value="structured">结构化地址</Radio>
        <Radio value="waybillSenderAddress">运单发件地址</Radio>
        <Radio value="waybillSenderName">运单发件名称</Radio>
        {fieldName.includes('SubTitle') && <Radio value="none">不展示</Radio>}
      </Radio.Group>
    </Form.Item>
  );

  const onFinish = (values: PolicyConfigFormData) => {
    // Combine form values with component state
    const formData: PolicyConfigFormData = {
      ...values,
      citySelections: cityRows.map(row => ({ type: row.type, city: row.cities.join(',') })),
      selectedCities,
      versionConfigs,
      selectedDigits,
      suffixType: selectedSuffixType
    };
    
    // Validate required fields based on mode
    if (values.displayMode === 'gray' && selectedCities.length === 0) {
      form.setFields([{
        name: 'displayMode',
        errors: ['请选择并添加城市']
      }]);
      return;
    }

    if (values.versionMode === 'gray' && versionConfigs.some(config => config.versions.length === 0)) {
      form.setFields([{
        name: 'versionMode',
        errors: ['请为每个平台选择版本']
      }]);
      return;
    }

    if (values.suffixMode === 'gray' && selectedDigits.length === 0) {
      form.setFields([{
        name: 'suffixMode',
        errors: ['请选择尾号']
      }]);
      return;
    }

    console.log('Form submitted:', formData);
  };

  const validateMessages = {
    required: '${label}不能为空',
  };

  return (
    <Form
      form={form}
      layout="vertical"
      className="max-w-4xl mx-auto p-6"
      onFinish={onFinish}
      validateMessages={validateMessages}
      initialValues={{
        displayMode: 'all',
        versionMode: 'all',
        suffixMode: 'all'
      }}
    >
      {/* Basic Strategy Section */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">基础策略</h2>
        
        {/* Before Order Section */}
        <div className="mb-6">
          <h3 className="text-base font-medium mb-3">接单前</h3>
          <Form.Item 
            name="beforeOrderMainTitle" 
            label="主标题内容类型"
            rules={[{ required: true }]}
          >
            {renderContentTypeRadioGroup('beforeOrderMainTitle')}
          </Form.Item>
          <Form.Item 
            name="beforeOrderSubTitle" 
            label="副标题内容类型"
            rules={[{ required: true }]}
          >
            {renderContentTypeRadioGroup('beforeOrderSubTitle')}
          </Form.Item>
        </div>

        {/* Waiting for Pickup Section */}
        <div className="mb-6">
          <h3 className="text-base font-medium mb-3">待取货</h3>
          <Form.Item 
            name="waitingPickupMainTitle" 
            label="主标题内容类型"
            rules={[{ required: true }]}
          >
            {renderContentTypeRadioGroup('waitingPickupMainTitle')}
          </Form.Item>
          <Form.Item 
            name="waitingPickupSubTitle" 
            label="副标题内容类型"
            rules={[{ required: true }]}
          >
            {renderContentTypeRadioGroup('waitingPickupSubTitle')}
          </Form.Item>
        </div>

        {/* Waiting for Delivery Section */}
        <div className="mb-6">
          <h3 className="text-base font-medium mb-3">待送达</h3>
          <Form.Item 
            name="waitingDeliveryMainTitle" 
            label="主标题内容类型"
            rules={[{ required: true }]}
          >
            {renderContentTypeRadioGroup('waitingDeliveryMainTitle')}
          </Form.Item>
          <Form.Item 
            name="waitingDeliverySubTitle" 
            label="副标题内容类型"
            rules={[{ required: true }]}
          >
            {renderContentTypeRadioGroup('waitingDeliverySubTitle')}
          </Form.Item>
        </div>
      </div>

      {/* Effective Range Section */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">生效范围</h2>
        
        {/* Display Range Subsection */}
        <div className="mb-6">
          <h3 className="text-base font-medium mb-3">展示范围</h3>
          <Form.Item 
            name="displayMode"
            rules={[{ required: true }]}
          >
            <Radio.Group onChange={handleDisplayModeChange} value={displayMode}>
              <Radio value="all">全量</Radio>
              <Radio value="gray">灰度</Radio>
            </Radio.Group>
          </Form.Item>
          
          {displayMode === 'gray' && (
            <div className="mt-4">
              {/* City Selection Rows */}
              {cityRows.map(row => (
                <div key={row.key} className="flex items-center gap-4 mb-4">
                  <Select
                    value={row.type}
                    onChange={(value) => handleTypeChange(row.key, value)}
                    className="w-24"
                  >
                    <Option value="加盟">加盟</Option>
                    <Option value="众包">众包</Option>
                  </Select>
                  <Select
                    mode="multiple"
                    value={row.cities}
                    onChange={(values) => handleCityChange(row.key, values)}
                    className="flex-1"
                    placeholder="选择城市"
                  >
                    {mockCities.map(city => (
                      <Option key={city} value={city}>{city}</Option>
                    ))}
                  </Select>
                  <Button onClick={() => addSelectedCities(row.key)}>添加</Button>
                  <Button 
                    type="text" 
                    icon={<PlusOutlined />} 
                    onClick={addCityRow}
                  />
                  <Button
                    type="text"
                    icon={<MinusCircleOutlined />}
                    onClick={() => removeCityRow(row.key)}
                    disabled={cityRows.length === 1}
                  />
                </div>
              ))}
              
              {/* Selected Cities Display */}
              <div className="mt-4">
                {selectedCities.map(city => (
                  <Tag
                    key={city}
                    closable
                    onClose={() => removeSelectedCity(city)}
                    className="mb-2 mr-2"
                  >
                    {city}
                  </Tag>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* System Version Subsection */}
        <div className="mb-6">
          <h3 className="text-base font-medium mb-3">系统版本</h3>
          <Form.Item 
            name="versionMode"
            rules={[{ required: true }]}
          >
            <Radio.Group onChange={handleVersionModeChange} value={versionMode}>
              <Radio value="all">全量</Radio>
              <Radio value="gray">灰度</Radio>
            </Radio.Group>
          </Form.Item>
          
          {versionMode === 'gray' && (
            <div className="mt-4">
              {versionConfigs.map((config) => (
                <div key={config.platform} className="mb-4">
                  <div className="flex items-center gap-4">
                    <span className="w-16">{config.platform === 'android' ? 'Android' : 'iOS'}</span>
                    <Select
                      value={config.logic}
                      onChange={(value) => handleVersionLogicChange(config.platform, value as VersionLogic)}
                      className="w-24"
                    >
                      <Option value="gt">&gt;</Option>
                      <Option value="lt">&lt;</Option>
                      <Option value="eq">=</Option>
                      <Option value="gte">≥</Option>
                      <Option value="lte">≤</Option>
                    </Select>
                    <Select
                      mode={config.logic === 'eq' ? 'multiple' : undefined}
                      value={config.versions}
                      onChange={(values) => handleVersionSelect(config.platform, Array.isArray(values) ? values : [values])}
                      className="flex-1"
                      placeholder="选择版本"
                    >
                      {mockVersions.map(version => (
                        <Option key={version} value={version}>{version}</Option>
                      ))}
                    </Select>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Suffix Restriction Subsection */}
        <div className="mb-6">
          <h3 className="text-base font-medium mb-3">尾号限制</h3>
          <Form.Item 
            name="suffixMode"
            rules={[{ required: true }]}
          >
            <Radio.Group onChange={handleSuffixModeChange} value={suffixMode}>
              <Radio value="all">全量</Radio>
              <Radio value="gray">灰度</Radio>
            </Radio.Group>
          </Form.Item>
          
          {suffixMode === 'gray' && (
            <div className="mt-4">
              <div className="flex items-center gap-4 mb-4">
                <Select
                  value={selectedSuffixType}
                  onChange={(value) => setSelectedSuffixType(value)}
                  className="w-32"
                >
                  {mockSuffixTypes.map(type => (
                    <Option key={type} value={type}>
                      {type === 'phone' ? '手机号' : type === 'riderId' ? '骑手ID' : '美团ID'}
                    </Option>
                  ))}
                </Select>
                <Select
                  mode="multiple"
                  value={selectedDigits}
                  onChange={setSelectedDigits}
                  className="flex-1"
                  placeholder="选择尾号"
                >
                  {mockDigits.map(digit => (
                    <Option key={digit} value={digit}>{digit}</Option>
                  ))}
                </Select>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Form Actions */}
      <div className="flex justify-end">
        <Space>
          <Button>取消</Button>
          <Button type="primary" htmlType="submit">
            确定
          </Button>
        </Space>
      </div>
    </Form>
  );
};

export default PolicyConfigForm;
