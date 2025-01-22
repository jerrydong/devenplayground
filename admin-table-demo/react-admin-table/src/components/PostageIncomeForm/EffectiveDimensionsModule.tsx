'use client';

import * as React from 'react';
import { useFormContext } from 'react-hook-form';
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,

} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { X, Plus, Minus } from 'lucide-react';
import {
  PostageIncomeFormData,
  SYSTEM_TYPES,
  COMPARISON_TYPES,
  RESTRICTION_TYPES,
  DISPLAY_ROLES,
} from './types';
import { mockCityData } from '@/services/mockCityApi';

interface CityRowType {
  id: string;
  type: string;
  cities: string[];
}

export function EffectiveDimensionsModule() {
  const { control, watch, setValue } = useFormContext<PostageIncomeFormData>();
  const [cityRows, setCityRows] = React.useState<CityRowType[]>([
    { id: '1', type: 'franchise', cities: [] },
  ]);

  // Watch for grayscale values
  const appVersionGrayscale = watch('effectiveDimensions.appVersion.isGrayscale');
  const cityRangeGrayscale = watch('effectiveDimensions.cityRange.isGrayscale');
  const riderNumberGrayscale = watch('effectiveDimensions.riderNumber.isGrayscale');
  const comparisonType = watch('effectiveDimensions.cityRange.comparison');

  // City row management
  const addCityRow = () => {
    const newId = (cityRows.length + 1).toString();
    setCityRows([...cityRows, { id: newId, type: 'franchise', cities: [] }]);
  };

  const removeCityRow = (id: string) => {
    setCityRows(cityRows.filter(row => row.id !== id));
  };

  const handleCitySelection = (rowId: string, type: string, selectedCities: string[]) => {
    setCityRows(rows =>
      rows.map(row =>
        row.id === rowId ? { ...row, type, cities: selectedCities } : row
      )
    );

    // Update form value
    const cityTags = cityRows.flatMap(row =>
      row.cities.map(city => ({ type: row.type, city }))
    );
    setValue('effectiveDimensions.appVersion.cities', cityTags);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>生效维度</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* APP Version */}
        <div className="space-y-4">
          <h3 className="font-medium">APP版本</h3>
          <FormField
            control={control}
            name="effectiveDimensions.appVersion.isGrayscale"
            render={({ field }) => (
              <FormItem className="flex flex-row items-center space-x-2">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <FormLabel className="font-normal">灰度</FormLabel>
              </FormItem>
            )}
          />

          {appVersionGrayscale && (
            <div className="space-y-4 border rounded-md p-4">
              <div className="space-y-4">
                {cityRows.map((row) => (
                  <div key={row.id} className="flex items-center space-x-4">
                    <select
                      className="border rounded p-2"
                      value={row.type}
                      onChange={(e) => handleCitySelection(row.id, e.target.value, row.cities)}
                    >
                      <option value="franchise">加盟</option>
                      <option value="crowdsourcing">众包</option>
                    </select>
                    <select
                      className="border rounded p-2"
                      multiple
                      value={row.cities}
                      onChange={(e) => {
                        const cities = Array.from(e.target.selectedOptions, option => option.value);
                        handleCitySelection(row.id, row.type, cities);
                      }}
                    >
                      {mockCityData.map(city => (
                        <option key={city.id} value={city.name}>
                          {city.name}
                        </option>
                      ))}
                    </select>
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => handleCitySelection(row.id, row.type, row.cities)}
                    >
                      添加
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => addCityRow()}
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                    {cityRows.length > 1 && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeCityRow(row.id)}
                      >
                        <Minus className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>
              <div className="flex flex-wrap gap-2 mt-4">
                {cityRows.flatMap(row =>
                  row.cities.map(city => (
                    <div
                      key={`${row.type}-${city}`}
                      className="flex items-center space-x-1 bg-zinc-100 rounded-full px-3 py-1"
                    >
                      <span>{`${row.type === 'franchise' ? '加盟' : '众包'}-${city}`}</span>
                      <button
                        onClick={() => {
                          handleCitySelection(
                            row.id,
                            row.type,
                            row.cities.filter(c => c !== city)
                          );
                        }}
                        className="ml-2"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* City Range */}
        <div className="space-y-4">
          <h3 className="font-medium">城市范围</h3>
          <FormField
            control={control}
            name="effectiveDimensions.cityRange.isGrayscale"
            render={({ field }) => (
              <FormItem className="flex flex-row items-center space-x-2">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <FormLabel className="font-normal">灰度</FormLabel>
              </FormItem>
            )}
          />

          {cityRangeGrayscale && (
            <div className="space-y-4 border rounded-md p-4">
              <FormField
                control={control}
                name="effectiveDimensions.cityRange.systems"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>系统类型</FormLabel>
                    <div className="flex gap-4">
                      {SYSTEM_TYPES.map((type) => (
                        <FormItem key={type.value} className="flex items-center space-x-2">
                          <FormControl>
                            <Checkbox
                              checked={field.value?.includes(type.value)}
                              onCheckedChange={(checked) => {
                                const value = field.value || [];
                                if (checked) {
                                  field.onChange([...value, type.value]);
                                } else {
                                  field.onChange(value.filter((v) => v !== type.value));
                                }
                              }}
                            />
                          </FormControl>
                          <FormLabel className="font-normal">{type.label}</FormLabel>
                        </FormItem>
                      ))}
                    </div>
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name="effectiveDimensions.cityRange.comparison"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>比较类型</FormLabel>
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        value={field.value}
                        className="flex gap-4"
                      >
                        {COMPARISON_TYPES.map((type) => (
                          <FormItem key={type.value} className="flex items-center space-x-2">
                            <FormControl>
                              <RadioGroupItem value={type.value} />
                            </FormControl>
                            <FormLabel className="font-normal">{type.label}</FormLabel>
                          </FormItem>
                        ))}
                      </RadioGroup>
                    </FormControl>
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name="effectiveDimensions.cityRange.versions"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>版本选择</FormLabel>
                    <FormControl>
                      <Input
                        placeholder={comparisonType === 'eq' ? '输入单个版本' : '输入版本，用逗号分隔'}
                        value={field.value?.join(',')}
                        onChange={(e) => {
                          const versions = e.target.value.split(',').map(v => v.trim());
                          if (comparisonType === 'eq') {
                            field.onChange([versions[0]]);
                          } else {
                            field.onChange(versions);
                          }
                        }}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />
            </div>
          )}
        </div>

        {/* Rider Number */}
        <div className="space-y-4">
          <h3 className="font-medium">骑手尾号</h3>
          <FormField
            control={control}
            name="effectiveDimensions.riderNumber.isGrayscale"
            render={({ field }) => (
              <FormItem className="flex flex-row items-center space-x-2">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <FormLabel className="font-normal">灰度</FormLabel>
              </FormItem>
            )}
          />

          {riderNumberGrayscale && (
            <div className="space-y-4 border rounded-md p-4">
              <FormField
                control={control}
                name="effectiveDimensions.riderNumber.restrictionType"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>限制类型</FormLabel>
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        value={field.value}
                        className="flex gap-4"
                      >
                        {RESTRICTION_TYPES.map((type) => (
                          <FormItem key={type.value} className="flex items-center space-x-2">
                            <FormControl>
                              <RadioGroupItem value={type.value} />
                            </FormControl>
                            <FormLabel className="font-normal">{type.label}</FormLabel>
                          </FormItem>
                        ))}
                      </RadioGroup>
                    </FormControl>
                  </FormItem>
                )}
              />

              <FormField
                control={control}
                name="effectiveDimensions.riderNumber.numbers"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>具体数字</FormLabel>
                    <div className="grid grid-cols-5 gap-4">
                      {Array.from({ length: 10 }, (_, i) => (
                        <FormItem key={i} className="flex items-center space-x-2">
                          <FormControl>
                            <Checkbox
                              checked={field.value?.includes(i)}
                              onCheckedChange={(checked) => {
                                const value = field.value || [];
                                if (checked) {
                                  field.onChange([...value, i]);
                                } else {
                                  field.onChange(value.filter((v) => v !== i));
                                }
                              }}
                            />
                          </FormControl>
                          <FormLabel className="font-normal">{i}</FormLabel>
                        </FormItem>
                      ))}
                    </div>
                  </FormItem>
                )}
              />
            </div>
          )}
        </div>

        {/* Display Role */}
        <div className="space-y-4">
          <h3 className="font-medium">展示角色</h3>
          <FormField
            control={control}
            name="effectiveDimensions.displayRole"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <RadioGroup
                    onValueChange={field.onChange}
                    value={field.value}
                    className="flex gap-4"
                  >
                    {DISPLAY_ROLES.map((role) => (
                      <FormItem key={role.value} className="flex items-center space-x-2">
                        <FormControl>
                          <RadioGroupItem value={role.value} />
                        </FormControl>
                        <FormLabel className="font-normal">{role.label}</FormLabel>
                      </FormItem>
                    ))}
                  </RadioGroup>
                </FormControl>
              </FormItem>
            )}
          />
        </div>
      </CardContent>
    </Card>
  );
}
